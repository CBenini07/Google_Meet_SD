# Server_Broker.py

import zmq
import signal
import sys

def main():
    context = zmq.Context()

    # 1) TEXTO: REP para receber, PUB para distribuir
    text_rep = context.socket(zmq.REP)
    text_rep.bind("tcp://*:5556")
    text_pub = context.socket(zmq.PUB)
    text_pub.bind("tcp://*:5555")

    # 2) ÁUDIO: PULL para receber, PUB para distribuir
    audio_pull = context.socket(zmq.PULL)
    audio_pull.bind("tcp://*:5566")
    audio_pub  = context.socket(zmq.PUB)
    audio_pub.bind("tcp://*:5567")

    # 3) VÍDEO: PULL para receber, PUB para distribuir
    video_pull = context.socket(zmq.PULL)
    video_pull.bind("tcp://*:5576")
    video_pub  = context.socket(zmq.PUB)
    video_pub.bind("tcp://*:5577")

    # Poller para multiplexar as três entradas
    poller = zmq.Poller()
    poller.register(text_rep,   zmq.POLLIN)
    poller.register(audio_pull, zmq.POLLIN)
    poller.register(video_pull, zmq.POLLIN)

    print("Broker rodando (texto:5556/5555, áudio:5566/5567, vídeo:5576/5577)...")

    def on_exit(signum, frame):
        print("\nEncerrando broker…")
        for sock in (text_rep, text_pub, audio_pull, audio_pub, video_pull, video_pub):
            sock.close(linger=0)
        context.term()
        sys.exit(0)

    signal.signal(signal.SIGINT, on_exit)
    signal.signal(signal.SIGTERM, on_exit)

    try:
        while True:
            socks = dict(poller.poll())

            # --- TEXTO --------------------------------------------------------
            if text_rep in socks:
                raw = text_rep.recv()       # b"CLIENT_ID:mensagem"
                text_rep.send(b"ok")
                text_pub.send(raw)

            # --- ÁUDIO --------------------------------------------------------
            if audio_pull in socks:
                sender, chunk = audio_pull.recv_multipart()
                audio_pub.send_multipart([sender, chunk])

            # --- VÍDEO --------------------------------------------------------
            if video_pull in socks:
                sender, frame = video_pull.recv_multipart()
                video_pub.send_multipart([sender, frame])

    except Exception as e:
        print("Erro no broker:", e)
    finally:
        on_exit(None, None)

if __name__ == "__main__":
    main()
