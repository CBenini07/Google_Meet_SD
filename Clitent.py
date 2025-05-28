# client.py
import zmq
import threading

NOME = input("Digite seu nome: ")

context = zmq.Context()

# Cliente envia mensagens para o servidor
socket_req = context.socket(zmq.REQ)
socket_req.connect("tcp://localhost:5556")

# Cliente escuta mensagens do servidor
socket_sub = context.socket(zmq.SUB)
socket_sub.connect("tcp://localhost:5555")
socket_sub.setsockopt_string(zmq.SUBSCRIBE, "")  # Inscreve em todas as mensagens

def receber():
    while True:
        msg = socket_sub.recv_string()
        print(f"\n{msg}\n> ", end='')

# Inicia thread de recepção
threading.Thread(target=receber, daemon=True).start()

# Envio de mensagens
while True:
    texto = input("> ")
    
    if texto.lower() == "stop":
        break
    
    socket_req.send_string(f"{NOME}: {texto}")
    socket_req.recv_string()  # espera confirmação do servidor

 # Encerra conexões e contexto
socket_pub.close()
socket_rep.close()
context.term()
print("[INFO]: Servidor finalizado com sucesso.")
