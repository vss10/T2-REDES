import socket
import threading
import random
import hashlib
import os
import tkinter as tk
from tkinter import scrolledtext, simpledialog
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Diffie-Hellman parameters (usar números grandes para produção)
P = 23  # Um número primo
G = 5   # Uma raiz primitiva de P

# Função para derivar uma chave de 16 bytes (AES-128) a partir da chave compartilhada
def derive_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:16]

# Cliente de Chat com Interface Gráfica
class ChatClient:
    def __init__(self, server_host="127.0.0.1", server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        self.client_private_key = random.randint(1, P - 1)
        self.client_public_key = pow(G, self.client_private_key, P)
        self.shared_key = None

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        self.root = tk.Tk()
        self.root.withdraw()  # Oculta a janela principal temporariamente

        self.username = simpledialog.askstring("Username", "Escolha seu username:")

        if not self.username:  # Caso o usuário cancele o input
            print("Nenhum username fornecido. Encerrando...")
            exit()

        self.root.deiconify()  # Mostra a janela principal após o input
        self.root.title(f"Chat Seguro - {self.username}")
        
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=20, width=50)
        self.chat_display.pack(padx=10, pady=10)
        
        self.entry_message = tk.Entry(self.root, width=40)
        self.entry_message.pack(padx=10, pady=5, side=tk.LEFT)
        
        self.send_button = tk.Button(self.root, text="Enviar", command=self.send_message)
        self.send_button.pack(padx=10, pady=5, side=tk.RIGHT)

        self.exchange_keys_and_communicate()

    def update_chat_display(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def receive_messages(self):
        try:
            while True:
                encrypted_data = self.client_socket.recv(1024)
                iv = encrypted_data[:16]  # Extrai o IV
                encrypted_message = encrypted_data[16:]  # Extrai a mensagem cifrada
                cipher = AES.new(self.shared_key, AES.MODE_CBC, iv=iv)
                decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode()
                self.update_chat_display(decrypted_message)
        except Exception as e:
            print(f"Erro ao receber mensagens: {e}")

    def send_message(self):
        message = self.entry_message.get()
        if message:
            iv = os.urandom(16)  # Gerando IV aleatório
            cipher = AES.new(self.shared_key, AES.MODE_CBC, iv=iv)
            encrypted_message = iv + cipher.encrypt(pad(message.encode(), AES.block_size))  # Prefixa IV
            self.client_socket.send(encrypted_message)
            self.entry_message.delete(0, tk.END)

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
        iv = os.urandom(16)  # Gerando IV aleatório para criptografia do username
        cipher = AES.new(self.shared_key, AES.MODE_CBC, iv=iv)
        encrypted_username = iv + cipher.encrypt(pad(self.username.encode(), AES.block_size))  # Prefixa IV
        self.client_socket.send(encrypted_username)

        # Iniciar thread para receber mensagens
        threading.Thread(target=self.receive_messages, daemon=True).start()
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient()
