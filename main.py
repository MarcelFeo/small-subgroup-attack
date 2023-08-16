from hashlib import sha256
import ecdsa
import base58
import requests

# definindo os parametros da curva elíptica (secp256k1)
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8

# criando uma curva
curve = ecdsa.ellipticcurve.CurveFp(p, a, b)
generator = ecdsa.ellipticcurve.Point(curve, Gx, Gy, n)

def generate_private_key():
    # gerando a chave privada "aleatoriamente" entre um intervalo [1, n]
    return ecdsa.util.randrange(1, n)

def generate_public_key(private_key):
    # gerando a chave pública
    return private_key * generator

def generate_bitcoin_address(public_key):
    public_key_bytes = public_key.to_string()
    sha256_hash = sha256(public_key_bytes).digest()
    ripemd160_hash = hashlib.new("ripemd160", sha256_hash).digest()
    address_bytes = b"\x00" + ripemd160_hash
    checksum = sha256(sha256(address_bytes).digest()).digest()[:4]
    bitcoin_address = base58.b58encode(address_bytes + checksum).decode("utf-8")
    return bitcoin_address

def check_address_in_blockchain(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    balance = int(response.text)
    return balance > 0

def main():
    num_keys_to_generate = 1000
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
        print(f"Public Key: {public_key}")
        print(f"Bitcoin Address: {bitcoin_address}")
        print()

if __name__ == "__main__":
    main()
