# Secure E-Voting System - Backend API

Flask-based backend API with Multi-Factor Authentication, Face Recognition, and Aadhaar validation.

## Features

- **Multi-Factor Authentication (MFA)**: OTP via Email/SMS
- **Face Recognition**: OpenCV + face_recognition library for biometric verification
- **Aadhaar Validation**: Verhoeff algorithm + mock API integration
- **Attack Detection**: Brute force detection, rate limiting, suspicious activity monitoring
- **Admin Alerts**: Real-time security alerts via email
- **Audit Logging**: Complete audit trail of all actions
- **JWT Authentication**: Secure token-based authentication

## Installation

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If `face-recognition` installation fails, install system dependencies first:

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev
```

**macOS:**
```bash
brew install cmake
```

### 3. Configuration

Create `.env` file from example:

```bash
cp .env.example .env
```

Edit `.env` and configure:

```env
SECRET_KEY=your-super-secret-key-change-this
ENCRYPTION_KEY=your-32-byte-encryption-key!!!!
JWT_SECRET=your-jwt-secret-key-change-this
DATABASE_URL=sqlite:///voting.db

# Email settings (for OTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=dipti.qriocity@gmail.com
```

**Gmail App Password Setup:**
1. Enable 2FA on your Gmail account
2. Go to: https://myaccount.google.com/apppasswords
3. Generate an app password
4. Use the generated password in `SMTP_PASSWORD`

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

## API Endpoints

### Authentication

#### 1. Register Voter
```http
POST /api/auth/register
Content-Type: application/json

{
  "wallet_address": "0x1234...",
  "aadhaar_number": "234567890123",
  "voter_id": "ABC1234567",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+919876543210"
}
```

#### 2. Register Face Biometrics
```http
POST /api/auth/register-face
Content-Type: application/json

{
  "wallet_address": "0x1234...",
  "face_image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

#### 3. Request OTP
```http
POST /api/auth/login/request-otp
Content-Type: application/json

{
  "wallet_address": "0x1234...",
  "otp_type": "email"
}
```

#### 4. Verify Login (OTP + Face)
```http
POST /api/auth/login/verify
Content-Type: application/json

{
  "wallet_address": "0x1234...",
  "otp_code": "123456",
  "face_image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```

#### 5. Get Voter Info
```http
GET /api/auth/voter/0x1234...
```

### Admin Endpoints (Requires JWT Token)

#### Get All Voters
```http
GET /api/admin/voters?page=1&per_page=50
Authorization: Bearer <jwt_token>
```

#### Get Statistics
```http
GET /api/admin/voters/stats
Authorization: Bearer <jwt_token>
```

#### Get Audit Logs
```http
GET /api/admin/audit-logs?action=login&status=success
Authorization: Bearer <jwt_token>
```

#### Get Security Alerts
```http
GET /api/admin/alerts?severity=high
Authorization: Bearer <jwt_token>
```

#### Resolve Alert
```http
POST /api/admin/alerts/1/resolve
Authorization: Bearer <jwt_token>
```

#### Unlock Account
```http
POST /api/admin/voters/1/unlock
Authorization: Bearer <jwt_token>
```

## Security Features

### 1. Aadhaar Validation
- Format validation (12 digits, cannot start with 0 or 1)
- Verhoeff checksum algorithm
- Mock API integration (replace with real UIDAI API in production)

### 2. Face Recognition
- Face detection using Haar Cascade
- Face encoding using dlib's 128-dimensional face descriptor
- Liveness detection (blur, brightness, uniformity checks)
- Configurable tolerance threshold

### 3. OTP System
- 6-digit random OTP
- Configurable expiry time (default: 5 minutes)
- Email and SMS support
- Automatic invalidation of old OTPs

### 4. Attack Detection
- **Brute Force Protection**: Lock account after 5 failed attempts (30 min)
- **Rate Limiting**: Max 5 OTP requests per 15 minutes
- **Suspicious Activity**: Detect rapid actions (10 in 1 minute)
- **IP-based Monitoring**: Track failed attempts from same IP

### 5. Admin Alerts
- Real-time email notifications
- Severity levels: low, medium, high, critical
- Alert types: brute_force, multiple_failed_login, suspicious_activity

## Database Schema

### Voters Table
- `id`, `wallet_address`, `aadhaar_number`, `voter_id`
- `name`, `email`, `phone`
- `is_registered`, `is_verified`, `has_voted`
- `failed_login_attempts`, `locked_until`

### Biometric Data Table
- `id`, `voter_id`
- `face_encoding` (JSON), `face_image_path`
- `fingerprint_hash`, `fingerprint_template`

### OTP Table
- `id`, `voter_id`, `otp_code`, `otp_type`
- `is_used`, `is_valid`, `expires_at`

### Audit Logs Table
- `id`, `voter_id`, `action`, `status`
- `ip_address`, `user_agent`, `details`, `timestamp`

### Attack Alerts Table
- `id`, `alert_type`, `severity`, `description`
- `ip_address`, `voter_id`, `is_resolved`, `notified`

## Testing

### Test Aadhaar Numbers (Valid Format)
```
234567890123
345678901234
456789012345
```

### Test Voter IDs
```
ABC1234567
DEF9876543
```

### Dev Mode
In development, OTPs are printed to console if SMTP is not configured.

## Production Deployment

1. **Database**: Switch from SQLite to PostgreSQL
   ```env
   DATABASE_URL=postgresql://user:password@localhost/voting_db
   ```

2. **HTTPS**: Use SSL certificates (Let's Encrypt)

3. **Environment Variables**: Use secure secrets management

4. **UIDAI Integration**: Replace mock API with real Aadhaar verification

5. **SMS Service**: Integrate Twilio/AWS SNS for SMS OTP

6. **Rate Limiting**: Add Redis for distributed rate limiting

7. **Gunicorn**: Use production WSGI server
   ```bash
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

## Troubleshooting

### face-recognition installation fails
Install dlib first:
```bash
pip install dlib
pip install face-recognition
```

### OpenCV errors
Install system dependencies:
```bash
sudo apt-get install python3-opencv
```

### Database errors
Reset database:
```bash
rm voting.db
python app.py  # Will recreate tables
```

## Support

For issues, contact: dipti.qriocity@gmail.com
