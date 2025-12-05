from .ecdsa_signature import (
    HashGeneration,
    ECDSA_KeyGeneration,
    Load_PrivateKey,
    Load_PublicKey,
    Sign_hash,
    save_signature,
    Load_signature,
    Verify_Signature,
)

import os
KEYS_DIR = r"C:\Users\HP\Desktop\Projet_Cryptographie\Projet-File-Integrity-Authentication-Tool\Keys"
PRIVATE_KEY_PATH = os.path.join(KEYS_DIR, "Private_Key.Pem")
PUBLIC_KEY_PATH = os.path.join(KEYS_DIR, "Public_Key.Pem")

__all__ = [
    'HashGeneration',
    'ECDSA_KeyGeneration',
    'Load_PrivateKey',
    'Load_PublicKey',
    'Sign_hash',
    'save_signature',
    'Load_signature',
    'Verify_Signature',
    'PRIVATE_KEY_PATH',
    'PUBLIC_KEY_PATH'
]