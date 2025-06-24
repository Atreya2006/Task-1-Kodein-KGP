# chat_server.py
import socket
import threading
import json
from rsa import generate_rsa_keys, decrypt_message

class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.clients = []
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(5)
        print(f"Server listening on {host}:{port}")
        # Generate one RSA key-pair for all clients
        self.public_key, self.private_key = generate_rsa_keys(bits=512)

    def broadcast(self, msg_bytes, exclude=None):
        for c in self.clients:
            if c is not exclude:
                try:
                    c.send(msg_bytes)
                except:
                    self.clients.remove(c)

    def handle_client(self, client_sock):
        try:
            # Step 1: receive raw name
            name = client_sock.recv(1024).decode().strip()
            print(f"> {name} joined")
            self.clients.append(client_sock)
            # Step 2: send public key as JSON
            client_sock.send(json.dumps({"public_key": self.public_key}).encode())

            # Step 3: loop receive encrypted messages
            while True:
                chunk = client_sock.recv(4096)
                if not chunk:
                    break
                data = json.loads(chunk.decode())
                encrypted = data.get("message")
                # decrypt and rebroadcast plaintext
                text = decrypt_message(self.private_key, encrypted)
                full = f"{name}: {text}"
                print(full)
                self.broadcast(full.encode(), exclude=client_sock)
        except Exception as e:
            print("Client error:", e)
        finally:
            client_sock.close()
            if client_sock in self.clients:
                self.clients.remove(client_sock)
            print(f"> {name} left")

    def start(self):
        try:
            while True:
                sock, addr = self.server.accept()
                threading.Thread(target=self.handle_client, args=(sock,), daemon=True).start()
        finally:
            self.server.close()

if __name__ == "__main__":
    ChatServer().start()
