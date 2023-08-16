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
