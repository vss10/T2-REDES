import socket
import threading
import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Diffie-Hellman parameters (usar números grandes para produção)
P = 23  # Um número primo
G = 5   # Uma raiz primitiva de P

# Função para derivar uma chave de 16 bytes (AES-128) a partir da chave compartilhada
def derive_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:16]

# Servidor de Chat
class ChatServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.server_private_key = random.randint(1, P - 1)
        self.server_public_key = pow(G, self.server_private_key, P)
        self.clients = {}  # Armazena (username, socket, chave compartilhada)

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor de chat em execução em {self.host}:{self.port}")

    def broadcast(self, message, sender_socket):
        for username, (client_socket, key) in self.clients.items():
            if client_socket != sender_socket:
                cipher = AES.new(key, AES.MODE_CBC, iv=bytes(16))
                encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
                client_socket.send(encrypted_message)

    def handle_client(self, client_socket, addr):
        print(f"Conexão aceita de {addr}")

        # Enviar a chave pública do servidor ao cliente
        client_socket.send(str(self.server_public_key).encode())

        # Receber a chave pública do cliente
        client_public_key = int(client_socket.recv(1024).decode())
        print(f"Chave pública do cliente recebida de {addr}: {client_public_key}")

        # Calcular a chave compartilhada
        shared_key = pow(client_public_key, self.server_private_key, P)
        print(f"Chave compartilhada com {addr}: {shared_key}")

        # Derivar chave AES
        aes_key = derive_key(shared_key)

        # Receber o username do cliente
        encrypted_username = client_socket.recv(1024)
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=bytes(16))
        username = unpad(cipher.decrypt(encrypted_username), AES.block_size).decode()
        print(f"Username recebido de {addr}: {username}")

        self.clients[username] = (client_socket, aes_key)

        # Comunicação do cliente
        try:
            while True:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break

                decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode()
                print(f"Mensagem de {username}: {decrypted_message}")

                # Verificar se a mensagem é apenas para o servidor
                if decrypted_message.startswith("/server"):
                    print(f"Mensagem para o servidor de {username}: {decrypted_message[8:]}")
                else:
                    # Enviar mensagem para todos os outros clientes
                    self.broadcast(f"{username}: {decrypted_message}", client_socket)
        except Exception as e:
            print(f"Erro com o cliente {username}: {e}")
        finally:
            print(f"Cliente {username} desconectado.")
            client_socket.close()
            del self.clients[username]

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server = ChatServer()
    server.start()