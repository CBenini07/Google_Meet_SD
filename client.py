# client.py

import threading
import uuid
import zmq
import cv2
import numpy as np
import sounddevice as sd

# Gere um ID único para este cliente:
CLIENT_ID = uuid.uuid4().hex[:6].encode()  # e.g. b'9fa3d2'

SERVER_IP = "192.168.15.3"

###############
# CONFIGURAÇÕES
###############
# áudio
CHUNK    = 512
CHANNELS = 1
RATE     = 16000
DTYPE    = 'int16'

# vídeo
FRAME_WIDTH  = 320
FRAME_HEIGHT = 240
JPEG_QUALITY = 50

def texto_send(ctx):
    req = ctx.socket(zmq.REQ)
    req.connect(f"tcp://{SERVER_IP}:5556")
    while True:
        msg = input()
        payload = CLIENT_ID + b":" + msg.encode()
        req.send(payload)
        req.recv()
        if msg.lower() == "stop":
            break

def texto_recv(ctx):
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://{SERVER_IP}:5555")
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    while True:
        raw = sub.recv()
        sender, text = raw.split(b":", 1)
        if sender != CLIENT_ID:
            print(f"[CHAT {sender.decode()}] {text.decode()}")

def audio_send(ctx):
    push = ctx.socket(zmq.PUSH)
    push.connect(f"tcp://{SERVER_IP}:5566")

    def callback(indata, frames, time, status):
        if status:
            print(f"Input status: {status}")
        # converte diretamente para bytes
        data_bytes = bytes(indata)
        push.send_multipart([CLIENT_ID, data_bytes])

    with sd.RawInputStream(samplerate=RATE,
                           blocksize=CHUNK,
                           dtype=DTYPE,
                           channels=CHANNELS,
                           callback=callback):
        threading.Event().wait()  # mantém o stream aberto

def audio_recv(ctx):
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://{SERVER_IP}:5567")
    sub.setsockopt(zmq.SUBSCRIBE, b"")

    stream = sd.RawOutputStream(samplerate=RATE,
                                blocksize=CHUNK,
                                dtype=DTYPE,
                                channels=CHANNELS)
    stream.start()
    try:
        while True:
            sender, chunk = sub.recv_multipart()
            if sender != CLIENT_ID:
                stream.write(chunk)
    except KeyboardInterrupt:
        pass
    finally:
        stream.stop()
        stream.close()

def video_send(ctx):
    push = ctx.socket(zmq.PUSH)
    push.connect(f"tcp://{SERVER_IP}:5576")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            _, buf = cv2.imencode('.jpg', frame,
                                  [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            push.send_multipart([CLIENT_ID, buf.tobytes()])
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()

def video_recv(ctx):
    sub = ctx.socket(zmq.SUB)
    sub.connect(f"tcp://{SERVER_IP}:5577")
    sub.setsockopt(zmq.SUBSCRIBE, b"")
    cv2.namedWindow("Video Remoto", cv2.WINDOW_NORMAL)
    try:
        while True:
            sender, data = sub.recv_multipart()
            if sender != CLIENT_ID:
                arr   = np.frombuffer(data, dtype=np.uint8)
                frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
                if frame is not None:
                    cv2.imshow("Video Remoto", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    ctx = zmq.Context()
    # threads de recepção
    threading.Thread(target=texto_recv, args=(ctx,), daemon=True).start()
    threading.Thread(target=audio_recv, args=(ctx,), daemon=True).start()
    threading.Thread(target=video_recv, args=(ctx,), daemon=True).start()
    # threads de envio
    threading.Thread(target=audio_send, args=(ctx,), daemon=True).start()
    threading.Thread(target=video_send, args=(ctx,), daemon=True).start()
    # thread principal: envio de texto
    texto_send(ctx)
    ctx.term()
