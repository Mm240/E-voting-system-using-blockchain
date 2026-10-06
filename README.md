# Smart Voting: Blockchain E-Voting with Voice & Sign Authentication

A secure electronic voting system that combines **Ethereum smart contracts** for tamper-proof vote storage with **multi-factor voter authentication** (wallet, OTP, face + Aadhaar photo match) and **accessible voting methods** (voice commands and hand-sign gestures).

## Features

- **Blockchain voting:** votes are recorded by a Solidity `Voting` contract; each voter can vote once, and results can be verified on-chain.
- **Wallet login:** MetaMask identifies voters and the admin.
- **Multi-factor authentication:** wallet, email OTP, face recognition and Aadhaar photo verification.
- **Aadhaar validation:** Verhoeff checksum check (can be relaxed in development).
- **Voice voting:** speak a candidate's name; speech-to-text with fuzzy name matching selects the candidate.
- **Sign-language voting:** show a hand sign to the camera; MediaPipe landmarks and a Random Forest classifier map it to a candidate.
- **Admin panel:** manage candidates, voters, votes, audit logs and security alerts; unlock or delete voters.
- **Attack detection:** rate limiting, brute-force detection, audit logging and alerts.
- **Multi-language UI:** i18next with a language switcher.
- **Attack simulation demo:** educational scripts that exercise the defences (see `attack_demo/`).

## Tech stack

| Layer | Tools |
|---|---|
| Frontend | React 19, Vite 7, Tailwind CSS 4, Radix UI, shadcn-style components, react-router, axios, i18next, ethers / web3.js |
| Backend | Python, Flask, Flask-SQLAlchemy, Flask-CORS, Flask-Bcrypt, PyJWT, pyotp, cryptography |
| Database | SQLite by default (`DATABASE_URL`); PostgreSQL supported via `psycopg2` |
| Biometrics / AI | OpenCV, `face_recognition` (dlib), MediaPipe Hands, scikit-learn (Random Forest), SpeechRecognition, pydub |
| Blockchain | Solidity 0.8.17, Truffle, Ganache (local chain), MetaMask |

## Project structure

```
backend/      Flask API (routes/, models/, utils/), trained sign model, SQLite DB (created locally)
frontend/     React app (src/components, src/api, src/abi, src/i18n)
blockchain/   Voting.sol contract, Truffle config and migrations
attack_demo/  Attack simulation scripts
```

### API overview

| Prefix | Purpose |
|---|---|
| `/api/auth` | register, face registration, Aadhaar photo check, OTP login |
| `/api/admin` | voters, votes, stats, audit logs, security alerts |
| `/api/voice` | speech recognition and voice vote |
| `/api/sign` | sign detection and sign vote |
| `/api/blockchain` | sync candidates with the chain |

## Getting started

### Prerequisites

- Python **3.11** (newer versions lack compatible `mediapipe` / `scikit-learn` builds for the bundled model)
- Node.js 18+
- `cmake` (for building `dlib`; on macOS: `brew install cmake`)
- Truffle (`npm i -g truffle`) and Ganache (`npx ganache`)
- Chrome / Brave / Firefox with the **MetaMask** extension

### 1. Local blockchain

```bash
npx ganache --port 8545 --chain.chainId 1337 --chain.networkId 1337 --wallet.deterministic
cd blockchain
truffle migrate --reset
cp build/contracts/Voting.json ../frontend/src/abi/Voting.json
```

The account that deploys the contract (Ganache account 0) is the **admin**.

### 2. Backend

```bash
cd backend
python3.11 -m venv venv && source venv/bin/activate
pip install "setuptools<81" Flask==3.0.0 Flask-CORS==4.0.0 Flask-SQLAlchemy==3.1.1 Flask-Bcrypt==1.0.1 \
  cryptography PyJWT==2.8.0 python-dotenv pyotp qrcode requests "numpy<2" opencv-python-headless Pillow \
  psycopg2-binary "mediapipe==0.10.21" "scikit-learn==1.2.2" joblib SpeechRecognition pydub web3 \
  face-recognition git+https://github.com/ageitgey/face_recognition_models
cp .env.example .env     # then edit values
python app.py            # http://localhost:8000
```

Set `ADMIN_WALLET` in `.env` to the admin wallet address (lowercase or checksummed). Without `SMTP_USER` / `SMTP_PASSWORD`, OTPs are not emailed; they are printed in the backend console (`[DEV MODE] OTP ...`).

### 3. Frontend

```bash
cd frontend
npm install
npm run dev              # http://localhost:5173
```

Set `VITE_BACKEND_URL` if the backend is not on `http://localhost:8000`.

### 4. MetaMask

1. Add a network: RPC `http://127.0.0.1:8545`, chain ID `1337`, symbol `ETH`.
2. Import a Ganache account's private key (use the admin account for admin access).
3. Open the app, connect the wallet, then register or log in (OTP, face, Aadhaar).

An admin must register a voter's wallet on-chain (`registerVoter`) and add candidates (`addCandidate`) before that voter can vote. Voting is allowed between the contract's `startTime` and `endTime`, set at deployment (see `blockchain/migrations/1_deploy_voting.js`).

## Configuration (`backend/.env`)

| Variable | Description |
|---|---|
| `SECRET_KEY`, `JWT_SECRET`, `ENCRYPTION_KEY` | Application secrets; change before real use |
| `DATABASE_URL` | e.g. `sqlite:///voting.db` |
| `ADMIN_WALLET`, `ADMIN_EMAIL` | Admin identity |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` | Email delivery for OTP and alerts |
| `OTP_EXPIRY_MINUTES`, `MAX_LOGIN_ATTEMPTS` | Authentication limits |

`.env` and the database are git-ignored. Never commit them.

## Security notes

- Biometric and personal data live in the local database; protect and encrypt it in any real deployment.
- Dev-mode shortcuts (OTP printed to console, optional Aadhaar checksum skip) must be disabled in production.
- This project is a prototype for education and demonstration, not a certified election system.

## Attack demo

`attack_demo/` contains scripts that simulate attacks (e.g. brute force) against a running local instance to show the detection and rate limiting. Use them only on your own system. See [attack_demo/README.md](attack_demo/README.md).

## Demo videos

Screen recordings of the system are included in the repository root (`*.mp4`).
