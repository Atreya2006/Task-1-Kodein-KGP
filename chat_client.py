# chat_client.py
import socket
import threading
import json
from rsa import encrypt_message

class ChatClient:
    def __init__(self, host='127.0.0.1', port=12345):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.public_key = None

    def receive_loop(self):
        while True:
            try:
                data = self.sock.recv(4096).decode()
                # try JSON parse
                try:
                    obj = json.loads(data)
                    if "public_key" in obj:
                        self.public_key = tuple(obj["public_key"])
                        print(f"[System] Received server public key: {self.public_key}")
                        continue
                except json.JSONDecodeError:
                    pass
                # fallback: plaintext broadcast
                print(data)
            except:
                print("[System] Disconnected.")
                break

    def send_loop(self):
        while True:
            msg = input()
            if not self.public_key:
                print("[!] Waiting for server public key...")
                continue
            encrypted = encrypt_message(self.public_key, msg)
            packet = json.dumps({"message": encrypted}).encode()
            self.sock.send(packet)

    def start(self, name):
        # send raw name
        self.sock.send(name.encode())
        threading.Thread(target=self.receive_loop, daemon=True).start()
        self.send_loop()

if __name__ == "__main__":
    name = input("Enter your name: ").strip()
    client = ChatClient()
    client.start(name)
