# Databricks notebook source
# MAGIC %md
# MAGIC Generate a call.csv file

# COMMAND ----------

import csv
import datetime
import random

# Define the number of rows to generate
num_rows = 10000

# Define the header row
header_row = ["id", "call_datetime", "src", "target", "agent", "start_time", "end_time", "call_type", "line_of_business"]

# Define the trailer row
trailer_row = ["TRAILER", num_rows, datetime.date.today().strftime("%Y-%m-%d")]

# Define the lists for the "src", "target", and "agent" columns
src_list = [f"s{i}" for i in range(1, 11)]
target_list = [f"t{i}" for i in range(1, 11)]
agent_list = ["jack", "tom", "amy", "kelly", "susan"]

# Generate the data rows
data_rows = []
for i in range(num_rows):
    call_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    src = random.choice(src_list)
    target = random.choice(target_list)
    agent = random.choice(agent_list)
    start_time = datetime.datetime.now() - datetime.timedelta(minutes=random.randint(0, 120))
    end_time = start_time + datetime.timedelta(minutes=random.randint(0, 60))
    call_type = random.choice(["Inbound", "Outbound"])
    line_of_business = random.choice(["Retail", "Finance", "Healthcare"])
    data_row = [i+1, call_datetime, src, target, agent, start_time, end_time, call_type, line_of_business]
    data_rows.append(data_row)

# Write the CSV file
filename = "calls.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header_row)
    writer.writerows(data_rows)
    writer.writerow(trailer_row)

print(f"CSV file with {num_rows} rows generated: {filename}")


# COMMAND ----------

!pip install azure-identity azure-keyvault-secrets cryptography

# COMMAND ----------

# MAGIC %md
# MAGIC Import the necessary modules:

# COMMAND ----------

import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# COMMAND ----------

# MAGIC %md
# MAGIC Generate an RSA key pair with a password-protected private key:

# COMMAND ----------

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

public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# COMMAND ----------

# MAGIC %md
# MAGIC Store the private key in Azure Key Vault:

# COMMAND ----------

credential = DefaultAzureCredential()

secret_client = SecretClient(
    vault_url="https://linwen-dev-vault.vault.azure.net/",
    credential=credential
)

secret_name = "my-test-rsa-private-key"

secret_client.set_secret(
    secret_name,
    private_key_protected.decode('utf-8')
)

# COMMAND ----------

# MAGIC %md
# MAGIC if you got access error please find the appid=xxxx and grant permision for this appid or principle

# COMMAND ----------

# MAGIC %md
# MAGIC Encrypt the file using the public key:

# COMMAND ----------

with open('call.csv', 'rb') as file:
    data = file.read()

public_key = serialization.load_pem_public_key(public_key)

encrypted_data = public_key.encrypt(
    data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open('call.csv.bin', 'wb') as file:
    file.write(encrypted_data)

# COMMAND ----------

# MAGIC %md
# MAGIC Retrieve the private key from Azure Key Vault and decrypt the file:

# COMMAND ----------

private_key_protected = secret_client.get_secret(secret_name).value.encode('utf-8')

private_key = serialization.load_pem_private_key(
    private_key_protected,
    password=password
)

with open('call.csv.bin', 'rb') as file:
    encrypted_data = file.read()

decrypted_data = private_key.decrypt(
    encrypted_data,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open('call.csv.txt', 'wb') as file:
    file.write(decrypted_data)
