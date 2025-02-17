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

# Cliente de Chat
class ChatClient:
    def __init__(self, server_host="127.0.0.1", server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        self.client_private_key = random.randint(1, P - 1)
        self.client_public_key = pow(G, self.client_private_key, P)
        self.shared_key = None

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

    def receive_messages(self):
        try:
            while True:
                encrypted_message = self.client_socket.recv(1024)
                cipher = AES.new(self.shared_key, AES.MODE_CBC, iv=bytes(16))
                decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode()
                print(f"\nMensagem recebida: {decrypted_message}")
                print("Digite sua mensagem (/server para enviar apenas ao servidor): ", end="", flush=True)
        except Exception as e:
            print(f"Erro ao receber mensagens: {e}")

    def exchange_keys_and_communicate(self):
        # Receber a chave pública do servidor
        server_public_key = int(self.client_socket.recv(1024).decode())
        print(f"Chave pública do servidor recebida: {server_public_key}")

        # Enviar a chave pública do cliente ao servidor
        self.client_socket.send(str(self.client_public_key).encode())

        # Calcular a chave compartilhada
        self.shared_key = pow(server_public_key, self.client_private_key, P)
        print(f"Chave compartilhada calculada pelo cliente: {self.shared_key}")

        # Derivar chave AES
        self.shared_key = derive_key(self.shared_key)

        # Enviar username ao servidor
        username = input("Escolha seu username: ")
        cipher = AES.new(self.shared_key, AES.MODE_CBC, iv=bytes(16))
        encrypted_username = cipher.encrypt(pad(username.encode(), AES.block_size))
        self.client_socket.send(encrypted_username)

        # Iniciar thread para receber mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()

        # Enviar mensagens ao servidor
        try:
            while True:
                print("Digite sua mensagem (/server para enviar apenas ao servidor): ", end="")
                message = input()
                encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
                self.client_socket.send(encrypted_message)
        except KeyboardInterrupt:
            print("Encerrando cliente...")
            self.client_socket.close()

if __name__ == "__main__":
    client = ChatClient()
    client.exchange_keys_and_communicate()