# server.py
import zmq

context = zmq.Context()
socket_pub = context.socket(zmq.PUB)
socket_pub.bind("tcp://*:5555")  # Servidor publica mensagens

socket_rep = context.socket(zmq.REP)
socket_rep.bind("tcp://*:5556")  # Servidor recebe mensagens de clientes

print("Servidor rodando...")

while True:
    # --- TEXTO --------------------------------------------------------
    msg = socket_rep.recv_string()  # recebe mensagem do cliente
    
    if msg == "stop":
        socket_rep.send_string("ok")    # envia resposta ao cliente
        break
    
    print(f"[RECEBIDO]: {msg}")
    socket_pub.send_string(msg)     # publica a mensagem para todos
    socket_rep.send_string("ok")  
    
    
    # --- ÁUDIO ----------------------------------------------------------
    
    # --- IMAGEM ---------------------------------------------------------
    
 # Encerra conexões e contexto
socket_pub.close()
socket_rep.close()
context.term()
print("[INFO]: Servidor finalizado com sucesso.")
