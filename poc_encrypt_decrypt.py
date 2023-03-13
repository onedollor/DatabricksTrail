# Databricks notebook source
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

password = b'123!Abc123'

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

private_key_protected = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(password)
)

public_key_bytes = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

public_key = private_key.public_key()

# Export the public key in PEM format
# public_key_pem = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )

#data = "test data".encode('utf-8')
data = b"test data"

encrypted_data = public_key.encrypt(plaintext=data, padding=padding.PKCS1v15())
decrypted_data = private_key.decrypt(
    encrypted_data,
    padding=padding.PKCS1v15()
)

print(decrypted_data)
