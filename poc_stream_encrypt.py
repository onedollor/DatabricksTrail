# Databricks notebook source
from rsa_key import public_key
from cryptography.hazmat.primitives.asymmetric import padding

import io
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.serialization import load_pem_public_key

# Generate a new symmetric key for the encryption of the stream data
symmetric_key = Fernet.generate_key()

# Encrypt the symmetric key using the recipient's public key
encrypted_symmetric_key = public_key.encrypt(symmetric_key, padding=padding.PKCS1v15())

# Initialize a symmetric encryption algorithm with the generated key
cipher = Fernet(symmetric_key)

# Read the stream data in chunks and encrypt each chunk using the symmetric encryption algorithm
chunk_size = 1024  # Set the chunk size according to your use case
encrypted_data = io.BytesIO()
with open('c:/data/calls.csv', 'rb') as f:
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        encrypted_chunk = cipher.encrypt(chunk)
        encrypted_data.write(encrypted_chunk)

print(encrypted_data)

# Save the encrypted data and the encrypted symmetric key to a file
with open('encrypted_stream_data', 'wb') as f:
    f.write(encrypted_data.getvalue())
with open('encrypted_symmetric_key', 'wb') as f:
    f.write(encrypted_symmetric_key)
