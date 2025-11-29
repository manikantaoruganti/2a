#!/usr/bin/env python3
from datetime import datetime, timezone
from app.seed_manager import read_seed
from app.totp_utils import generate_totp


def main():
    try:
        hex_seed = read_seed()
    except:
        print("ERROR: seed not found", flush=True)
        return

    code = generate_totp(hex_seed)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - 2FA Code: {code}", flush=True)


if __name__ == "__main__":
    main()
