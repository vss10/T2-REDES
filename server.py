import socket
import threading
import random
import hashlib
import os
import tkinter as tk
from tkinter import scrolledtext
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Diffie-Hellman parameters (usar números grandes para produção)
P = 23  # Um número primo
G = 5   # Uma raiz primitiva de P

def derive_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:16]

class ChatServer:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.server_private_key = random.randint(1, P - 1)
        self.server_public_key = pow(G, self.server_private_key, P)
        self.clients = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        
        self.root = tk.Tk()
        self.root.title("Servidor de Chat Seguro")
        
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, state='disabled', height=20, width=50)
        self.chat_display.pack(padx=10, pady=10)
        
        threading.Thread(target=self.start, daemon=True).start()
        self.root.mainloop()

    def update_chat_display(self, message, color="black"):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message + "\n", (color,))
        self.chat_display.tag_config(color, foreground=color)
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def broadcast(self, message, sender_socket):
        for username, (client_socket, key) in self.clients.items():
            if client_socket != sender_socket:
                iv = os.urandom(16)
                cipher = AES.new(key, AES.MODE_CBC, iv=iv)
                encrypted_message = iv + cipher.encrypt(pad(message.encode(), AES.block_size))
                client_socket.send(encrypted_message)

    def handle_client(self, client_socket, addr):
        self.update_chat_display(f"Conexão aceita de {addr}")
        client_socket.send(str(self.server_public_key).encode())

        client_public_key = int(client_socket.recv(1024).decode())
        shared_key = pow(client_public_key, self.server_private_key, P)
        aes_key = derive_key(shared_key)

        encrypted_username = client_socket.recv(1024)
        iv = encrypted_username[:16]
        encrypted_username = encrypted_username[16:]
        cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
        username = unpad(cipher.decrypt(encrypted_username), AES.block_size).decode()
        self.update_chat_display(f"{username} entrou no chat.")
        self.clients[username] = (client_socket, aes_key)

        try:
            while True:
                encrypted_data = client_socket.recv(1024)
                if not encrypted_data:
                    break
                iv = encrypted_data[:16]
                encrypted_message = encrypted_data[16:]
                cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
                decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode()
                
                if decrypted_message.startswith("/server"):
                    self.update_chat_display(f"[Mensagem privada] {username}: {decrypted_message[8:]}", "red")
                else:
                    self.update_chat_display(f"{username}: {decrypted_message}")
                    self.broadcast(f"{username}: {decrypted_message}", client_socket)
        except Exception as e:
            self.update_chat_display(f"Erro com {username}: {e}")
        finally:
            self.update_chat_display(f"{username} saiu do chat.")
            client_socket.close()
            del self.clients[username]

    def start(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    ChatServer()
