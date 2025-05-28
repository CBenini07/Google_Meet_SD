from socket import *

# 1. Criar o socket
s = socket(AF_INET, SOCK_STREAM)

# 2. Associar o socket a um endereço (host, porta)
s.bind(('localhost', 12345))  # ou use '' para aceitar conexões externas

# 3. Colocar o socket em modo de escuta
s.listen(1)  # 1 = número máximo de conexões pendentes

print("Aguardando conexão...")

# 4. Aceitar a conexão
conn, addr = s.accept()
print(f"Conectado por {addr}")

# 5. Loop para receber e responder dados
while True:
    data = conn.recv(1024)
    if not data:
        break
    conn.send((data.decode() + "*").encode())

# 6. Fechar conexões
conn.close()
s.close()
