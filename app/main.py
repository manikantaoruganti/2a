from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.crypto_utils import load_private_key, decrypt_seed_hex
from app.totp_utils import generate_totp, remaining_validity, verify_totp
from app.seed_manager import read_seed, write_seed
import os

app = FastAPI()

DATA_PATH = "/data/seed.txt"
PRIVATE_KEY_PATH = "/app/student_private.pem"


class DecryptRequest(BaseModel):
    encrypted_seed: str


class VerifyRequest(BaseModel):
    code: str


@app.post("/decrypt-seed")
def decrypt_seed(req: DecryptRequest):
    try:
        private_key = load_private_key(PRIVATE_KEY_PATH)
        hex_seed = decrypt_seed_hex(req.encrypted_seed, private_key)
        write_seed(hex_seed)
        return {"status": "ok"}
    except Exception as e:
        print("Decryption error:", e)
        raise HTTPException(status_code=500, detail="Decryption failed")


@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = read_seed()
    code = generate_totp(hex_seed)
    valid_for = remaining_validity()
    return {"code": code, "valid_for": valid_for}


@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if req.code is None:
        raise HTTPException(status_code=400, detail="Missing code")

    if not os.path.exists(DATA_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")

    hex_seed = read_seed()
    is_valid = verify_totp(hex_seed, req.code)
    return {"valid": is_valid}
