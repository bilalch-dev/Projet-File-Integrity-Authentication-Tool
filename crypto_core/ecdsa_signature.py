# Implémentation de la signature ECDSA et SHA-256
import os
import hashlib
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec 
from cryptography.hazmat.primitives import hashes
import getpass
import base64
from cryptography.exceptions import InvalidSignature
import cryptography
import cryptography.hazmat.primitives.asymmetric.ec
import cryptography.hazmat.primitives.hashes
import cryptography.hazmat.primitives.serialization

def HashGeneration(file_path):
    if os.path.exists(file_path):
        with open(file_path,"rb") as file:
            content=file.read()
            hasher=hashlib.sha256()
            hasher.update(content)
            file_hash=hasher.hexdigest()
            return file_hash
    else:
        print("File doesn't exist !!!!!")
file_hash=HashGeneration(r"C:\Users\HP\Desktop\STP.txt")

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
ECDSA_KeyGeneration()

def Load_PrivateKey(path):
    passwd=getpass.getpass("Enter your password for the private key: ").encode()
    try:    
        with open(path,"rb") as file:
            PrivateKey=serialization.load_pem_private_key(
            data=file.read(),
            password=passwd,
        )
        return PrivateKey
    except Exception as e:
        print("❌ Your password is incorrect, or the key is invalid.")
        return None
PrivateKey=Load_PrivateKey(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys\Private_Key.Pem")

def Load_PublicKey(path):
    with open(path,"rb") as file:
        data=file.read()
        publicKey=serialization.load_pem_public_key(data)
        return publicKey
PublicKey=Load_PublicKey(r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys\Public_Key.Pem")

def Sign_hash(PrivateKey,file_hash):
    if PrivateKey is None:
        print("Impossible de signer : clé privée non chargée.")
        exit()
    hash_bytes=bytes.fromhex(file_hash)
    signature=PrivateKey.sign(hash_bytes, ec.ECDSA(hashes.SHA256()))
    signature_encoded=base64.b64encode(signature)
    return signature_encoded
Signature=Sign_hash(PrivateKey,file_hash)

def Verify_Signature(Signature,PublicKey,file_hash):
    hash_bytes=bytes.fromhex(file_hash)
    signature_decoded=base64.b64decode(Signature)
    try:
        PublicKey.verify(signature_decoded,hash_bytes,ec.ECDSA(hashes.SHA256()))
        print("Signature is Valid")
        return True
    except InvalidSignature:
        print("Signature is invalid")
        return False
Verify_Signature(Signature,PublicKey,file_hash)