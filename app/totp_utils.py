import pyotp
import base64
import time


def hex_to_base32(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    return base64.b32encode(seed_bytes).decode()


def generate_totp(hex_seed: str) -> str:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30, digest="sha1")
    return totp.now()


def verify_totp(hex_seed: str, code: str) -> bool:
    b32 = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(b32, digits=6, interval=30, digest="sha1")
    return totp.verify(code, valid_window=1)


def remaining_validity() -> int:
    return 30 - (int(time.time()) % 30)
