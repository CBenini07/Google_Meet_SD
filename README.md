# Google\_Meet\_SD

Trabalho 1 da matéria de Sistemas Distribuídos

João Rafael de Freitas Guimarães - 800295  
Cauã Benini - 801046

## Demonstração

https://github.com/user-attachments/assets/490c9155-d427-44c2-a0e7-ffde28068369

## Dependências

```bash
pip install -r requirements.txt
```
## Configuração

### Obtendo o IP da Máquina A

Para descobrir rapidamente o IP local:

* **Linux/macOS**:

  ```bash
  hostname -I
  ```
  
  ou
  
  ```bash
  ip addr show
  ```

* **Windows (PowerShell)**:

  ```powershell
  Get-NetIPAddress -AddressFamily IPv4 | Select-Object -ExpandProperty IPAddress
  ```

### Ajuste do SERVER\_IP

Edite o arquivo `client.py` em **ambas** as máquinas (A e B) e defina a variável `SERVER_IP` para o IP da Máquina A (onde o broker/servidor está rodando):

```python
SERVER_IP = "<IP_DA_MAQUINA_A>"
```

* Na **Máquina A**, use o próprio IP local obtido com os comandos anteriores.
* Na **Máquina B**, utilize esse mesmo IP da Máquina A.

## Como rodar

### Máquina A

1. No diretório do projeto, inicie o broker/servidor:

   ```bash
   python3 Server_Broker.py
   ```
2. Em outro terminal (mesmo diretório), execute o cliente:

   ```bash
   python3 client.py 2>/dev/null
   ```

### Máquina B

* No diretório do projeto, execute apenas o cliente:

  ```bash
  python3 client.py 2>/dev/null
  ```

> **Observação:** o redirecionamento `2>/dev/null` descarta mensagens de alerta do ALSA, mantendo o console limpo.
