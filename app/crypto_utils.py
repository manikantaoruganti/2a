import base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def load_private_key(path: str):
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def load_public_key(path: str):
    with open(path, "rb") as f:
        return load_pem_public_key(f.read())


def decrypt_seed_hex(encrypted_b64: str, private_key) -> str:
    encrypted_bytes = base64.b64decode(encrypted_b64)
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    hex_seed = decrypted.decode().strip()

    if len(hex_seed) != 64:
        raise ValueError("Invalid hex seed length")
    if not all(c in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Invalid hex seed characters")

    return hex_seed
