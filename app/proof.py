import base64
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding as pad
from cryptography.hazmat.primitives import hashes


def sign_commit_hash(commit_hash: str, priv_path: str) -> bytes:
    with open(priv_path, "rb") as f:
        private_key = load_pem_private_key(f.read(), password=None)

    sig = private_key.sign(
        commit_hash.encode(),
        pad.PSS(
            mgf=pad.MGF1(hashes.SHA256()),
            salt_length=pad.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return sig


def encrypt_signature(sig: bytes, pub_path: str) -> str:
    with open(pub_path, "rb") as f:
        pub = load_pem_public_key(f.read())

    encrypted = pub.encrypt(
        sig,
        pad.OAEP(
            mgf=pad.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode()


if __name__ == "__main__":
    import subprocess

    commit_hash = subprocess.check_output(
        ["git", "log", "-1", "--format=%H"]
    ).decode().strip()

    sig = sign_commit_hash(commit_hash, "student_private.pem")
    encrypted_sig = encrypt_signature(sig, "instructor_public.pem")

    print("\nCommit Hash:", commit_hash)
    print("\nEncrypted Signature (submit this):")
    print(encrypted_sig)
