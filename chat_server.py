import socket
import threading
import random
import math

# RSA functions (same as provided)
def is_prime(number):
    if number < 2:
        return False
    #By definition 1 is not a prime number
    for i in range(2, int(math.sqrt(number)) + 1): #checking if a divisor exists only till root of number to reduce time complexity
        if number % i == 0:
            return False
        #If no divisors exists then number is prime and so return true
    return True

#Function to generate prime numbers between min and max values
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    #Randomly generating numbers 
    while not is_prime(prime): #Keep generating untill the generated number is not prime
        prime = random.randint(min_value, max_value)
    return prime

def mod_inverse(e, phi): #Here, e is the public key (known by others), phi is the value of Euler's Totient Function(not known by others)
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
        #d is the Private key generated for the passed value of the public key e
    raise ValueError("Mod_inverse does not exist!")

def generate_rsa_keys(min_value=1000, max_value=50000):
    p, q = generate_prime(min_value, max_value), generate_prime(min_value, max_value)
    while p == q:
        q = generate_prime(min_value, max_value)
        #Keep generating p and q untill you get 2 non equal prime numbers
    n = p * q
    phi_n = (p - 1) * (q - 1) #Value of the Euler Totient Function

    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)
        #Finding a Public Key for the given phi value
    d = mod_inverse(e, phi_n)

    return (e, n), (d, n)  # public key, private key

#Function to encrypt the messages using the Public Key and RSA Algo
def encrypt_message(public_key, message):
    e, n = public_key
    encrypted_message = [pow(ord(char), e, n) for char in message]
    return encrypted_message

#Function decrypt the messages using the Private Key and RSA Algo
def decrypt_message(private_key, encrypted_message):
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in encrypted_message])
    return decrypted_message

# Chatroom server
class ChatServer:
    def __init__(self, host='127.0.0.1', port=12345):
        self.clients = []
        self.names = {}
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #TCP connection , use dgram instead to establish UDP
        self.server.bind((host, port))
        self.server.listen(5)
        print("Server started...")
        
    def broadcast(self, message, client_socket):
        for client in self.clients:
            if client != client_socket:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def handle_client(self, client_socket):
        try:
            name = client_socket.recv(1024).decode() #conversion 
            self.names[client_socket] = name
            public_key, private_key = generate_rsa_keys()
            client_socket.send(f"Your public key: {public_key}".encode())
            client_socket.send(f"Your private key: {private_key}".encode())
            
            while True:
                try:
                    message = client_socket.recv(1024)
                    if not message:
                        break
                    decrypted_message = decrypt_message(private_key, eval(message.decode()))
                    print(f"{name}: {decrypted_message}")
                    self.broadcast(message, client_socket)
                except:
                    client_socket.close()
                    self.clients.remove(client_socket)
                    break
        except Exception as e:
            print(f"Error handling client: {e}")
            client_socket.close()
            if client_socket in self.clients:
                self.clients.remove(client_socket)

    def start(self):
        try:
            while True:
                client_socket, client_address = self.server.accept()
                print(f"Connection from {client_address}")
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start() #starting the thread
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.server.close()

# Run the server
if __name__ == "__main__":
    server = ChatServer() # server object
    server.start()
