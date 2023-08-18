import hashlib
import random
import ecdsa
import base58
import requests
import secrets

INF_POINT = None

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.points = []
        #self.definePoints()  # Define os pontos que satisfazem a equação da curva elíptica

    def definePoints(self):
        self.points.append(INF_POINT)
        for x in range(self.p):
            for y in range(self.p):
                if self.equal_modp(y * y, x * x * x + self.a * x + self.b):
                    self.points.append((x, y))

    def print_points(self):
        print(self.points)

    def number_points(self):
        return len(self.points)

    def reduce_modp(self, x):
        return x % self.p

    def equal_modp(self, x, y):
        return self.reduce_modp(x - y) == 0

    def inverse_modp(self, x):
        if self.reduce_modp(x) == 0:
            return None
        return pow(x, self.p - 2, self.p)  # Fixed: Use self.p instead of p

    # Operações

    def add(self, P1, P2):
        if P1 == INF_POINT:
            return P2
        if P2 == INF_POINT:
            return P1

        x1 = P1[0]
        x2 = P2[0]
        y1 = P1[1]
        y2 = P2[1]

        if self.equal_modp(x1, x2) and self.equal_modp(y1, -y2):
            return INF_POINT

        if self.equal_modp(x1, x2) and self.equal_modp(y1, y2):
            m = self.reduce_modp((3 * x1 * x1 + self.a) * self.inverse_modp(2 * y1))  # Fixed: Use x1 * x1 instead of x1 * x2
        else:
            m = self.reduce_modp((y1 - y2) * self.inverse_modp(x1 - x2))  # Fixed: Use x1 - x2 instead of x1 * x2

        v = self.reduce_modp(y1 - m * x1)
        x3 = self.reduce_modp(m * m - x1 - x2)
        y3 = self.reduce_modp(-m * x3 - v)

        return (x3, y3)

    def test_associativity(self):
        n = len(self.points)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    p = self.add(self.points[i], self.add(self.points[j], self.points[k]))
                    q = self.add(self.add(self.points[i], self.points[j]), self.points[k])
                    if p != q:
                        return False
        return True

    def mul(self, k, P):
        Q = INF_POINT
        if k == 0:
            return Q
        while k != 0:
            if k & 1 != 0:
                Q = self.add(Q, P)
            P = self.add(P, P)
            k >>= 1
        return Q

    def is_point_on_curve(self, x, y):
        return self.equal_modp(y * y, x * x * x + self.a * x + self.b)

# Define the parameters of the elliptic curve secp256k1 in Bitcoin
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

curve = EllipticCurve(a, b, p)
generator = (Gx, Gy)

def generate_private_key():
    # Generate a random private key within the range [1, n-1]
    num = random.randint(1, n - 1)  # Fixed: Generate between 1 and n-1
    return num

def generate_public_key(private_key):
    # Generate the corresponding public key using ECDSA
    return curve.mul(private_key, generator)  # Fixed: Use curve.mul instead of curve

def generate_bitcoin_address(public_key):
    public_key_bytes = str(public_key)
    sha = hashlib.new('sha256')
    sha256_hash = sha.update(public_key_bytes)
    ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()  # Fixed: Use hashlib.new instead of new
    address_bytes = b"\x00" + ripemd160_hash
    checksum = hashlib.sha256(hashlib.sha256(address_bytes).digest()).digest()[:4]
    bitcoin_address = base58.b58encode(address_bytes + checksum).decode("utf-8")
    return bitcoin_address

def check_address_in_blockchain(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    balance = int(response.text)
    return balance > 0

num_keys_to_generate = 10
subgroup_attack_addresses = []

for _ in range(num_keys_to_generate):
    private_key = generate_private_key()
    public_key = generate_public_key(private_key)
    bitcoin_address = generate_bitcoin_address(public_key)

    if check_address_in_blockchain(bitcoin_address):
        subgroup_attack_addresses.append((private_key, public_key, bitcoin_address))

print("Subgroup Attack Addresses:")
for private_key, public_key, bitcoin_address in subgroup_attack_addresses:
    print(f"Private Key: {private_key}")
    print(f"Public Key: ({public_key[0]}, {public_key[1]})")  # Fixed: Use tuple indexing
    print(f"Bitcoin Address: {bitcoin_address}")
    print()
