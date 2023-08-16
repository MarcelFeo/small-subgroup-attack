from hashlib import sha256
import ecdsa
import base58
import requests

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
