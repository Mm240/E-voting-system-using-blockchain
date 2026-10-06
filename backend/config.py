import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Use absolute path to ensure we use the correct database file
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{os.path.join(BASE_DIR, "voting.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', 'default-key-32-bytes-long!!!!!!!')
    OTP_EXPIRY_MINUTES = int(os.getenv('OTP_EXPIRY_MINUTES', 5))
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', 20))
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'dipti.qriocity@gmail.com')
    ADMIN_WALLET = os.getenv('ADMIN_WALLET', '').lower()  # Admin wallet address (lowercase)

    # Face recognition settings
    FACE_RECOGNITION_TOLERANCE = 0.6
    FACE_IMAGES_DIR = 'static/face_images'

    # SMTP settings for email OTP
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')

    # Aadhaar validation (mock for development)
    AADHAAR_API_ENABLED = os.getenv('AADHAAR_API_ENABLED', 'False').lower() == 'true'
