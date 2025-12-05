# Implémentation de la signature ECDSA et SHA-256
from cryptography.hazmat.primitives.asymmetric.utils import Prehashed
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import ec 
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
import hashlib
import base64
import os

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

def ECDSA_KeyGeneration():
    courbe=ec.SECP256R1()
    PrivateKey=ec.generate_private_key(courbe)
    PublicKey=PrivateKey.public_key()
    Pem_PrivateKey=PrivateKey.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(b"yasseralloufi")
    )
    keys_dir = r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys"
    os.makedirs(keys_dir, exist_ok=True)
    
    private_key_path = os.path.join(keys_dir, "Private_Key.Pem")
    with open(private_key_path,"wb") as file:
        file.write(Pem_PrivateKey)
        print("Private key saved to private_key.pem in PEM format.")
    
    Pem_PublicKey=PublicKey.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    public_key_path = os.path.join(keys_dir, "Public_Key.Pem")
    with open(public_key_path,"wb") as file:
        file.write(Pem_PublicKey)
        print("Public key saved to public_key.pem in PEM format.")
    
    return private_key_path, public_key_path

def Load_PrivateKey(path,passwd=None):
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

def Load_PublicKey(path):
    with open(path,"rb") as file:
        data=file.read()
        publicKey=serialization.load_pem_public_key(data)
        return publicKey

def Sign_hash(PrivateKey,file_hash):
    if PrivateKey is None:
        print("Impossible de signer : clé privée non chargée.")
        return None
    hash_bytes=bytes.fromhex(file_hash)
    signature=PrivateKey.sign(hash_bytes, ec.ECDSA(Prehashed(hashes.SHA256())))
    signature_encoded=base64.b64encode(signature)
    return signature_encoded

def save_signature(file_path, Signature):
    sig_path = file_path + ".sig"
    try:
        signature_bytes = base64.b64decode(Signature)
        with open(sig_path, "wb") as f:
            f.write(signature_bytes)
        print(f"✅ Signature sauvegardée → {os.path.basename(sig_path)}")
        return sig_path
    except Exception as e:
        print(f"❌ Échec sauvegarde : {e}")
        return None

def Load_signature(sig_path):
    if not os.path.exists(sig_path):
        print(f"❌ Fichier signature introuvable : {sig_path}")
        return None
    try:
        with open(sig_path, "rb") as f:
            signature_bytes = f.read()
        print(f"✅ Signature chargée ({len(signature_bytes)} octets)")
        return signature_bytes
    except Exception as e:
        print(f"❌ Erreur lors du chargement de la signature : {e}")
        return None

def Verify_Signature(Signature_bytes, PublicKey, file_hash):
    try:
        hash_bytes = bytes.fromhex(file_hash)
        PublicKey.verify(
            Signature_bytes,
            hash_bytes,
            ec.ECDSA(Prehashed(hashes.SHA256()))
        )
        print("✅ Signature is Valid")
        return True
    except InvalidSignature:
        print("❌ Signature is invalid")
        return False
