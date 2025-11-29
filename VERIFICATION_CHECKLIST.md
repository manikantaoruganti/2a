# PKI 2FA Microservice - Verification Checklist

## Pre-Submission Verification

### ✓ File Structure
- [x] app/main.py - FastAPI endpoints
- [x] app/crypto_utils.py - RSA encryption/decryption
- [x] app/totp_utils.py - TOTP generation/verification
- [x] app/seed_manager.py - Persistent seed storage
- [x] app/proof.py - Commit proof generation
- [x] app/requirements.txt - Python dependencies
- [x] scripts/log_2fa_cron.py - Cron job script
- [x] cron/2fa-cron - Cron configuration (LF line endings)
- [x] Dockerfile - Multi-stage build
- [x] docker-compose.yml - Container orchestration
- [x] .gitattributes - Line ending configuration
- [x] student_private.pem - RSA 4096-bit private key
- [x] student_public.pem - RSA 4096-bit public key
- [x] instructor_public.pem - Instructor's public key (placeholder)

### ✓ Cryptography Requirements

**RSA Key Generation**
- [x] Key size: 4096 bits
- [x] Public exponent: 65537
- [x] Format: PEM
- [x] Private key stored in student_private.pem
- [x] Public key stored in student_public.pem

**Encryption (RSA/OAEP-SHA256)**
- [x] Padding: OAEP
- [x] MGF: MGF1 with SHA-256
- [x] Hash: SHA-256
- [x] Label: None
- [x] Used for: Seed decryption

**Signature (RSA-PSS-SHA256)**
- [x] Padding: PSS
- [x] MGF: MGF1 with SHA-256
- [x] Hash: SHA-256
- [x] Salt Length: Maximum (PSS.MAX_LENGTH)
- [x] Used for: Commit hash signing

### ✓ API Endpoints

**POST /decrypt-seed**
- [x] Accepts base64-encoded encrypted seed
- [x] Decrypts using RSA/OAEP-SHA256
- [x] Stores seed to /data/seed.txt
- [x] Returns {"status": "ok"} on success
- [x] Returns {"error": "Decryption failed"} with 500 on failure
- [x] Validates hex seed (64 characters, 0-9a-f)

**GET /generate-2fa**
- [x] Reads seed from /data/seed.txt
- [x] Generates current TOTP code
- [x] Calculates remaining validity seconds
- [x] Returns {"code": "123456", "valid_for": 30}
- [x] Returns 500 error if seed not found

**POST /verify-2fa**
- [x] Accepts {"code": "123456"}
- [x] Validates code parameter exists
- [x] Verifies against stored seed
- [x] Implements ±1 period tolerance (±30 seconds)
- [x] Returns {"valid": true/false}
- [x] Returns 400 if code missing
- [x] Returns 500 if seed not found

### ✓ TOTP Implementation

- [x] Algorithm: SHA-1
- [x] Period: 30 seconds
- [x] Digits: 6
- [x] Seed conversion: Hex to base32
- [x] Verification window: ±1 period
- [x] Time calculation: Correct epoch-based

### ✓ Docker Implementation

**Dockerfile**
- [x] Multi-stage build (builder + runtime)
- [x] Base image: python:3.11-slim
- [x] TZ=UTC environment variable
- [x] Cron daemon installed
- [x] Timezone data installed
- [x] Volume mount points: /data, /cron
- [x] Port exposed: 8080
- [x] Key files copied (private, public, instructor)

**docker-compose.yml**
- [x] Service definition with build context
- [x] Port mapping: 8080:8080
- [x] Named volumes: seed-data, cron-output
- [x] Volume mounts: /data, /cron
- [x] Environment: TZ=UTC
- [x] Restart policy: unless-stopped

### ✓ Persistent Storage

- [x] Seed stored at /data/seed.txt
- [x] Docker volume mounted at /data
- [x] Cron output at /cron/last_code.txt
- [x] Docker volume mounted at /cron
- [x] Volumes persist across restarts
- [x] Proper file permissions (755 for directories)

### ✓ Cron Job

- [x] Cron file: cron/2fa-cron
- [x] Line endings: LF (verified with .gitattributes)
- [x] Execution: Every minute
- [x] Script path: /app/scripts/log_2fa_cron.py
- [x] Output format: YYYY-MM-DD HH:MM:SS - 2FA Code: XXXXXX
- [x] Timestamp timezone: UTC
- [x] Log file: /cron/last_code.txt
- [x] Error handling: Graceful on missing seed

### ✓ Git Configuration

- [x] .gitattributes file exists
- [x] cron/2fa-cron line ending set to LF
- [x] .gitignore excludes encrypted_seed.txt
- [x] .gitignore excludes __pycache__/
- [x] .gitignore excludes *.pyc
- [x] student_private.pem committed
- [x] student_public.pem committed
- [x] instructor_public.pem committed
- [x] All source files committed
- [x] Dockerfile committed
- [x] docker-compose.yml committed

### ✓ Testing Checklist

Before submission, verify:

- [ ] Build Docker image successfully: `docker-compose build`
- [ ] Container starts: `docker-compose up -d`
- [ ] API responds on port 8080
- [ ] POST /decrypt-seed with valid seed: returns {"status": "ok"}
- [ ] GET /generate-2fa: returns code with valid_for
- [ ] POST /verify-2fa with correct code: returns {"valid": true}
- [ ] POST /verify-2fa with wrong code: returns {"valid": false}
- [ ] Container restart preserves seed
- [ ] Cron job runs (wait 70+ seconds, check /cron/last_code.txt)
- [ ] Cron entries have UTC timestamps
- [ ] Timezone verified as UTC: `docker exec <container> date`

### ✓ Submission Preparation

Gather these items:
1. [ ] GitHub repository URL (must match seed request)
2. [ ] Commit hash (40 characters): `git log -1 --format=%H`
3. [ ] Encrypted signature: `python3 app/proof.py`
4. [ ] Student public key: contents of `student_public.pem`
5. [ ] Encrypted seed: contents of `encrypted_seed.txt`

### ✓ Common Mistakes to Avoid

- [ ] Repository URL matches between seed request and submission
- [ ] Public key formatted correctly in API request (\n for newlines)
- [ ] Encrypted signature has NO line breaks (single line base64)
- [ ] Wrong encryption/decryption parameters (OAEP, PSS, SHA-256)
- [ ] TOTP seed converted to base32 (not used as raw hex)
- [ ] Cron file uses LF line endings (verified)
- [ ] Timezone is UTC everywhere
- [ ] Seed stored in Docker volume (not container filesystem)
- [ ] Proper error handling (HTTP status codes, JSON responses)
- [ ] Signing commit hash as ASCII (not binary)

## Testing Commands

```bash
# Build
docker-compose build

# Start
docker-compose up -d

# Test decrypt
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"

# Test generate
curl http://localhost:8080/generate-2fa

# Test verify
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"$CODE\"}"

# Check cron (after 70+ seconds)
sleep 70
docker exec $(docker ps -q) cat /cron/last_code.txt

# Verify UTC timezone
docker exec $(docker ps -q) date

# Stop
docker-compose down
```

## Submission Checklist

Before final submission:

- [ ] All files committed and pushed to GitHub
- [ ] Repository URL is public and accessible
- [ ] Docker builds without errors
- [ ] All three endpoints working correctly
- [ ] TOTP codes verify successfully
- [ ] Cron job logging every minute
- [ ] Seed persists after restart
- [ ] Timezone is UTC
- [ ] Commit proof generated
- [ ] All required information gathered
