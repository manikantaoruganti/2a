# PKI 2FA Microservice - Setup Guide

## Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI endpoints
│   ├── crypto_utils.py      # RSA/OAEP encryption
│   ├── totp_utils.py        # TOTP generation
│   ├── seed_manager.py      # Seed persistence
│   ├── proof.py             # Commit proof generation
│   └── requirements.txt
├── scripts/
│   └── log_2fa_cron.py      # Cron job script
├── cron/
│   └── 2fa-cron             # Cron configuration (LF line endings)
├── student_private.pem      # ✓ Generated (4096-bit RSA)
├── student_public.pem       # ✓ Generated
├── instructor_public.pem    # Placeholder (replace with actual)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Container orchestration
├── .gitattributes           # LF line ending enforcement
└── README_PKI_2FA.md
```

## Step 1: Prepare Repository

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial PKI 2FA microservice"
git remote add origin https://github.com/yourusername/your-repo-name
git push -u origin main
```

## Step 2: Get Your Public Key

Your `student_public.pem` is already generated and ready. View it:

```bash
cat student_public.pem
```

## Step 3: Request Encrypted Seed

Call the instructor API:

```bash
curl -X POST https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "YOUR_STUDENT_ID",
    "github_repo_url": "https://github.com/yourusername/your-repo-name",
    "public_key": "-----BEGIN PUBLIC KEY-----\n...\n-----END PUBLIC KEY-----\n"
  }'
```

**Important**: Format the public key with `\n` characters (not actual newlines) in JSON.

Python helper:
```python
import json
with open("student_public.pem", "r") as f:
    pub_key = f.read()

print(json.dumps({
    "student_id": "YOUR_STUDENT_ID",
    "github_repo_url": "https://github.com/yourusername/your-repo-name",
    "public_key": pub_key
}, indent=2))
```

## Step 4: Save Encrypted Seed

Save the API response's `encrypted_seed` field:

```bash
echo "BASE64_ENCRYPTED_SEED_FROM_API" > encrypted_seed.txt
```

## Step 5: Replace Instructor Public Key

Download the actual instructor public key and replace the placeholder:

```bash
# Remove placeholder
rm instructor_public.pem

# Add actual key
echo "-----BEGIN PUBLIC KEY-----
MIIBIjANBg...
...
-----END PUBLIC KEY-----" > instructor_public.pem
```

## Step 6: Build Docker Image

```bash
docker-compose build
```

## Step 7: Run Microservice

```bash
docker-compose up -d
```

Check logs:
```bash
docker-compose logs -f
```

## Step 8: Test Endpoints

### Test 1: Decrypt Seed
```bash
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"
```

Expected: `{"status": "ok"}`

### Test 2: Generate 2FA
```bash
curl http://localhost:8080/generate-2fa
```

Expected: `{"code": "123456", "valid_for": 27}`

### Test 3: Verify Valid Code
```bash
CODE=$(curl -s http://localhost:8080/generate-2fa | jq -r '.code')
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"$CODE\"}"
```

Expected: `{"valid": true}`

### Test 4: Verify Invalid Code
```bash
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"code": "000000"}'
```

Expected: `{"valid": false}`

### Test 5: Check Cron Job (wait 70+ seconds)
```bash
sleep 70
docker exec $(docker ps -q) cat /cron/last_code.txt
```

Expected: Multiple lines with timestamps and codes

## Step 9: Verify Seed Persistence

```bash
# Restart container
docker-compose restart

# Seed should still work
curl http://localhost:8080/generate-2fa
```

## Step 10: Generate Commit Proof

```bash
# Make sure all changes are committed
git add -A
git commit -m "Add encrypted seed"

# Generate proof
python3 app/proof.py
```

Output:
```
Commit Hash: abc123...
Encrypted Signature (submit this):
BASE64_ENCRYPTED_SIGNATURE...
```

## Step 11: Prepare Submission

Gather these items:
1. **GitHub Repository URL**: `https://github.com/yourusername/your-repo-name`
2. **Commit Hash**: From `git log -1 --format=%H`
3. **Encrypted Signature**: From `python3 app/proof.py`
4. **Student Public Key**: Contents of `student_public.pem`
5. **Encrypted Seed**: Contents of `encrypted_seed.txt`

## Troubleshooting

### "Decryption failed"
- Check that encrypted_seed.txt is valid
- Verify you used the correct student_public.pem when requesting seed
- Ensure repo URL matches exactly

### TOTP codes don't verify
- Check cron job is running: `docker exec $(docker ps -q) cat /cron/last_code.txt`
- Verify TZ=UTC is set: `docker exec $(docker ps -q) echo $TZ`
- Wait for seed to be decrypted first

### Cron job not running
- Check file permissions: `ls -la cron/2fa-cron`
- Verify LF line endings: `file cron/2fa-cron`
- Check container logs: `docker-compose logs`

### Volume errors
- Clean up old containers: `docker-compose down -v`
- Rebuild: `docker-compose build --no-cache`

## Key Files

- `student_private.pem` - **COMMIT TO GIT** (required for Docker build)
- `student_public.pem` - **COMMIT TO GIT** (required for submission)
- `instructor_public.pem` - **COMMIT TO GIT** (required)
- `encrypted_seed.txt` - **DO NOT COMMIT** (sensitive data)

## Security Notes

- These RSA keys will be public in your repository
- Do NOT reuse these keys for any other purpose
- Consider them compromised once committed
- Generate new keys for production use
