import random
import math

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
