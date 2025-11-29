# PKI-based 2FA Microservice

Secure authentication microservice demonstrating enterprise-grade security practices through Public Key Infrastructure (PKI) and Time-based One-Time Password (TOTP) two-factor authentication.

## Features

- **RSA 4096-bit Encryption**: Secure seed transmission using RSA/OAEP-SHA256
- **TOTP 2FA**: RFC 6238 compliant time-based one-time passwords with 30-second intervals
- **Docker Containerization**: Multi-stage build with cron job automation
- **Persistent Storage**: Docker volumes ensure seed and logs survive container restarts
- **REST API**: Three endpoints for seed decryption, 2FA generation, and verification

## Architecture

### API Endpoints

- `POST /decrypt-seed` - Decrypt and store encrypted seed
- `GET /generate-2fa` - Generate current TOTP code
- `POST /verify-2fa` - Verify TOTP code with ±1 period tolerance

### Technology Stack

- **Framework**: FastAPI (Python)
- **Cryptography**: cryptography library (RSA/OAEP, RSA-PSS)
- **TOTP**: pyotp (SHA-1, 30s period, 6-digit codes)
- **Container**: Docker with cron daemon
- **Storage**: Docker named volumes

## Setup

1. **Install Docker Compose**
   ```bash
   docker-compose build
   ```

2. **Request Encrypted Seed**
   - Get your student ID and GitHub repository URL
   - Call instructor API with your `student_public.pem`
   - Save response to `encrypted_seed.txt`

3. **Run the Microservice**
   ```bash
   docker-compose up -d
   ```

4. **Test Endpoints**
   ```bash
   # Decrypt seed
   curl -X POST http://localhost:8080/decrypt-seed \
     -H "Content-Type: application/json" \
     -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"

   # Generate 2FA code
   curl http://localhost:8080/generate-2fa

   # Verify code
   curl -X POST http://localhost:8080/verify-2fa \
     -H "Content-Type: application/json" \
     -d '{"code": "123456"}'
   ```

## File Structure

```
.
├── app/
│   ├── main.py              # FastAPI endpoints
│   ├── crypto_utils.py      # RSA encryption/decryption
│   ├── totp_utils.py        # TOTP generation/verification
│   ├── seed_manager.py      # Persistent seed storage
│   ├── proof.py             # Commit signing utility
│   └── requirements.txt
├── scripts/
│   └── log_2fa_cron.py      # Cron job script
├── cron/
│   └── 2fa-cron             # Cron configuration
├── Dockerfile
├── docker-compose.yml
└── README_PKI_2FA.md
```

## Security Considerations

- RSA 4096-bit keys with 65537 public exponent
- OAEP padding for all encryption operations
- PSS padding for digital signatures
- UTC timezone for timestamp consistency
- 30-second TOTP period with ±1 window tolerance
- Persistent storage in Docker volumes

## Cron Job

Automatically generates and logs 2FA codes every minute to `/cron/last_code.txt` in UTC format.
