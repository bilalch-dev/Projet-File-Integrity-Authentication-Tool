import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend


def derive_key(password: bytes, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LEN,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password)


def file_encryption(input_file_path: str, output_file_path: str, password: str):
    with open(input_file_path, "rb") as f:
        target_file = f.read()

    salt = os.urandom(SALT_SIZE)
    key = derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    nonce = os.urandom(NONCE_SIZE)
    encrypted_content = aesgcm.encrypt(nonce, target_file, None)

    with open(output_file_path, "wb") as f:
        f.write(MAGIC + salt + nonce + encrypted_content)


def file_decryption(input_file_path: str, output_file_path: str, password: str):
    with open(input_file_path, "rb") as f:
        encrypted_data = f.read()

    if len(encrypted_data) < len(MAGIC) + SALT_SIZE + NONCE_SIZE:
        raise ValueError("File too short or corrupted")

    magic = encrypted_data[:4]
    if magic != MAGIC:
        raise ValueError("Unrecognized file format or version")

    salt = encrypted_data[4:4 + SALT_SIZE]
    nonce = encrypted_data[4 + SALT_SIZE:4 + SALT_SIZE + NONCE_SIZE]
    ciphertext = encrypted_data[4 + SALT_SIZE + NONCE_SIZE:]

    key = derive_key(password.encode(), salt)
    aesgcm = AESGCM(key)
    decrypted_content = aesgcm.decrypt(nonce, ciphertext, None)

    with open(output_file_path, "wb") as f:
        f.write(decrypted_content)


# Example usage
#file_encryption("class_schedule.pdf", "class_schedule_encrypted.pdf.aeg", "bilal")
file_decryption("class_schedule_encrypted.pdf.aeg", "class_schedule_decrypted.pdf", "bilal")
