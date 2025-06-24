# rsa.py
import random
import math

# Sieve of Eratosthenes for small prime filtering
def sieve(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    return [i for i, val in enumerate(is_prime) if val]

# Miller–Rabin Primality Test
def is_probable_prime(n, k=5):
    if n < 2:
        return False
    for p in [2,3,5,7,11,13,17,19,23,29]:
        if n % p == 0:
            return n == p
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Generate a large prime
def generate_large_prime(bit_length, sieve_limit=100000):
    small_primes = sieve(sieve_limit)
    while True:
        candidate = random.getrandbits(bit_length)
        candidate |= (1 << (bit_length - 1)) | 1
        if any(candidate % p == 0 for p in small_primes):
            continue
        if is_probable_prime(candidate):
            return candidate

# Extended Euclidean Algorithm
def mod_inverse(e, phi):
    def egcd(a, b):
        if b == 0:
            return a, 1, 0
        g, x1, y1 = egcd(b, a % b)
        return g, y1, x1 - (a // b) * y1
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist!")
    return x % phi

# RSA key gen
def generate_rsa_keys(bits=1024):
    p = generate_large_prime(bits // 2)
    q = generate_large_prime(bits // 2)
    while p == q:
        q = generate_large_prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n)

# Encrypt/decrypt UTF-8 messages
def encrypt_message(public_key, message: str):
    e, n = public_key
    data = message.encode('utf-8')
    return [pow(b, e, n) for b in data]

def decrypt_message(private_key, encrypted: list):
    d, n = private_key
    data = bytes(pow(c, d, n) for c in encrypted)
    return data.decode('utf-8')
