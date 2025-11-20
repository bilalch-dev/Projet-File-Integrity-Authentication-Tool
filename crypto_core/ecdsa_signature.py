# Implémentation de la signature ECDSA et SHA-256
import os
import hashlib
import base64
import cryptography
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec 
from cryptography.hazmat.backends import default_backend
import getpass
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization

def HashGeneration(file_path):
    if os.path.exists(file_path):
        with open(file_path,"rb") as file:
            content=file.read()
            hasher=hashlib.sha256()
            hasher.update(content)
            hexadec=hasher.hexdigest()
            return hexadec
    else:
        print("File doesn't exist !!!!!")
HashGeneration(r"C:\Users\HP\Desktop\STP.txt")

def ECDSA_KeyGeneration():
    courbe=ec.SECP256R1()
    PrivateKey=ec.generate_private_key(courbe)
    PublicKey=PrivateKey.public_key()
    Pem_PrivateKey=PrivateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"yasseralloufi")
    )
    os.makedirs(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys", exist_ok=True)
    with open(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys\Private_Key.Pem","wb") as file:
        file.write(Pem_PrivateKey)
        print("Private key saved to private_key.pem in PEM format.")
    
    Pem_PublicKey=PublicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys\Public_Key.Pem","wb") as file:
        file.write(Pem_PublicKey)
        print("Public key saved to public_key.pem in PEM format.")
#ECDSA_KeyGeneration()

def Load_PrivateKey(path):
    passwd=getpass.getpass("Enter your password for the private key: ").encode()
    try:    
        with open(path,"rb") as file:
            PrivateKey=serialization.load_pem_private_key(
            data=file.read(),
            password=passwd,
            backend=default_backend()
        )
        return PrivateKey
    except Exception as e:
        print("❌ Your password is incorrect, or the key is invalid.")

Load_PrivateKey(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys\Private_Key.Pem")