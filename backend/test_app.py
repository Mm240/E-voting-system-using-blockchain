"""
Simple test app to verify backend works without face recognition
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models.voter import db, Voter
from utils.aadhaar_service import validate_aadhaar_number, mock_aadhaar_api_verification
from utils.otp_service import create_otp, verify_otp
from utils.security_service import log_action
from datetime import datetime, timedelta
import jwt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})

# Health check
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Backend API is running (Test Mode - No Face Recognition)'
    }), 200

# Root endpoint
@app.route('/', methods=['GET'])
def root():
    return jsonify({
        'name': 'E-Voting System API (Test Mode)',
        'version': '1.0.0-test',
        'features': {
            'aadhaar_validation': True,
            'otp_mfa': True,
            'face_recognition': False
        }
    }), 200

# Register voter (without face)
@app.route('/api/auth/register', methods=['POST'])
def register_voter():
    try:
        data = request.json

        wallet_address = data.get('wallet_address', '').lower()
        aadhaar_number = data.get('aadhaar_number', '')
        name = data.get('name', '')
        email = data.get('email', '')

        if not wallet_address or not aadhaar_number or not name:
            return jsonify({'error': 'Missing required fields'}), 400

        # Validate Aadhaar
        aadhaar_valid, aadhaar_result = validate_aadhaar_number(aadhaar_number)
        if not aadhaar_valid:
            return jsonify({'error': aadhaar_result}), 400

        aadhaar_clean = aadhaar_result

        # Check if wallet already registered
        existing_voter = Voter.query.filter_by(wallet_address=wallet_address).first()
        if existing_voter:
            return jsonify({'error': 'Wallet address already registered'}), 400

        # Verify Aadhaar
        verification_result = mock_aadhaar_api_verification(aadhaar_clean, name)
        if not verification_result['verified']:
            return jsonify({'error': verification_result['message']}), 400

        # Create new voter
        voter = Voter(
            wallet_address=wallet_address,
            aadhaar_number=aadhaar_clean,
            voter_id=data.get('voter_id'),
            name=name,
            email=email,
            phone=data.get('phone'),
            is_registered=True,
            is_verified=True  # Auto-verify in test mode
        )

        db.session.add(voter)
        db.session.commit()

        log_action(voter.id, 'register', 'success', 'Voter registered (test mode)')

        return jsonify({
            'success': True,
            'message': 'Registration successful (Test Mode)',
            'voter': voter.to_dict(),
            'aadhaar_verification': verification_result
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

# Request OTP
@app.route('/api/auth/login/request-otp', methods=['POST'])
def request_otp():
    try:
        data = request.json
        wallet_address = data.get('wallet_address', '').lower()

        voter = Voter.query.filter_by(wallet_address=wallet_address).first()
        if not voter:
            return jsonify({'error': 'Voter not registered'}), 404

        # Create OTP
        otp = create_otp(voter.id, 'email', Config.OTP_EXPIRY_MINUTES)

        # In test mode, return OTP in response
        print(f"[TEST MODE] OTP for {voter.name}: {otp.otp_code}")

        return jsonify({
            'success': True,
            'message': f'OTP sent to email',
            'otp_code': otp.otp_code,  # Only for testing
            'expires_in_minutes': Config.OTP_EXPIRY_MINUTES
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500

# Verify login
@app.route('/api/auth/login/verify', methods=['POST'])
def verify_login():
    try:
        data = request.json
        wallet_address = data.get('wallet_address', '').lower()
        otp_code = data.get('otp_code', '')

        voter = Voter.query.filter_by(wallet_address=wallet_address).first()
        if not voter:
            return jsonify({'error': 'Voter not found'}), 404

        # Verify OTP
        otp_valid, otp_message = verify_otp(voter.id, otp_code, 'email')
        if not otp_valid:
            return jsonify({'error': otp_message}), 401

        # Generate JWT token
        token = jwt.encode({
            'voter_id': voter.id,
            'wallet_address': voter.wallet_address,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, Config.JWT_SECRET_KEY, algorithm='HS256')

        log_action(voter.id, 'login', 'success', 'Login successful (test mode)')

        return jsonify({
            'success': True,
            'message': 'Authentication successful (Test Mode)',
            'token': token,
            'voter': voter.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'Login verification failed: {str(e)}'}), 500

# Get voter info
@app.route('/api/auth/voter/<wallet_address>', methods=['GET'])
def get_voter_info(wallet_address):
    try:
        wallet_address = wallet_address.lower()
        voter = Voter.query.filter_by(wallet_address=wallet_address).first()

        if not voter:
            return jsonify({'error': 'Voter not found'}), 404

        return jsonify({
            'success': True,
            'voter': voter.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to get voter info: {str(e)}'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║   E-Voting System - TEST MODE Backend API           ║
    ║   Running on: http://localhost:8000                  ║
    ║   Face Recognition: DISABLED (Testing Only)          ║
    ╚═══════════════════════════════════════════════════════╝

    Test Endpoints:
    - POST /api/auth/register              - Register voter
    - POST /api/auth/login/request-otp     - Request OTP
    - POST /api/auth/login/verify          - Verify OTP
    - GET  /api/auth/voter/<wallet>        - Get voter info
    - GET  /health                         - Health check

    Test Aadhaar: 234567890123, 345678901234, 456789012345
    """)

    app.run(host='0.0.0.0', port=8000, debug=True)
