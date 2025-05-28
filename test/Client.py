from socket import *

HOST = 'localhost'  # ou o IP do servidor, ex: '192.168.1.100'
PORT = 12345        # mesma porta que o servidor está usando

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
s.send(b'Hello World')  # string codificada como bytes
data = s.recv(1024)

print(data.decode())  # decodifica os bytes recebidos para string
s.close()
