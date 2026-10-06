# from flask import Flask, jsonify
# from flask_cors import CORS
# from config import Config
# from models.voter import db, bcrypt
# from routes.auth_routes import auth_bp
# from routes.admin_routes import admin_bp
# import os

# def create_app(config_class=Config):
#     app = Flask(__name__)
#     app.config.from_object(config_class)

#     # Initialize extensions
#     db.init_app(app)
#     bcrypt.init_app(app)
#     CORS(app, resources={r"/*": {"origins": "*"}})

#     # Register blueprints
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(admin_bp, url_prefix='/api/admin')

#     # Health check endpoint
#     @app.route('/health', methods=['GET'])
#     def health_check():
#         return jsonify({
#             'status': 'healthy',
#             'message': 'Secure E-Voting Backend API is running'
#         }), 200

#     # Root endpoint
#     @app.route('/', methods=['GET'])
#     def root():
#         return jsonify({
#             'name': 'Secure E-Voting System API',
#             'version': '1.0.0',
#             'endpoints': {
#                 'auth': '/api/auth',
#                 'admin': '/api/admin',
#                 'health': '/health'
#             }
#         }), 200

#     # Error handlers
#     @app.errorhandler(404)
#     def not_found(error):
#         return jsonify({'error': 'Endpoint not found'}), 404

#     @app.errorhandler(500)
#     def internal_error(error):
#         return jsonify({'error': 'Internal server error'}), 500

#     # Create database tables
#     with app.app_context():
#         db.create_all()
#         print("Database tables created successfully")

#     return app


# if __name__ == '__main__':
#     app = create_app()

#     # Get port from environment or default to 8000
#     port = int(os.getenv('PORT', 8000))

#     print(f"""
#     ╔═══════════════════════════════════════════════════════╗
#     ║   Secure E-Voting System - Backend API Server       ║
#     ║   Version: 1.0.0                                     ║
#     ║   Running on: http://localhost:{port}                  ║
#     ╚═══════════════════════════════════════════════════════╝

#     API Endpoints:
#     - POST   /api/auth/register              - Register new voter
#     - POST   /api/auth/register-face         - Register face biometrics
#     - POST   /api/auth/login/request-otp     - Request OTP for login
#     - POST   /api/auth/login/verify          - Verify OTP and face
#     - GET    /api/auth/voter/<wallet>        - Get voter info

#     Admin Endpoints:
#     - GET    /api/admin/voters               - Get all voters
#     - GET    /api/admin/voters/stats         - Get voter statistics
#     - GET    /api/admin/audit-logs           - Get audit logs
#     - GET    /api/admin/alerts               - Get security alerts
#     - POST   /api/admin/alerts/<id>/resolve  - Resolve alert
#     - POST   /api/admin/voters/<id>/unlock   - Unlock account
#     - DELETE /api/admin/voters/<id>          - Delete voter

#     Press CTRL+C to stop the server
#     """)

#     app.run(host='0.0.0.0', port=port, debug=True)


from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models.voter import db, bcrypt
from routes.auth_routes import auth_bp
from routes.admin_routes import admin_bp
from routes.sign_routes import sign_bp
from routes.voice_routes import voice_bp
from routes.blockchain_sync_routes import sync_bp
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(sign_bp, url_prefix='/api/sign')
    app.register_blueprint(voice_bp, url_prefix='/api/voice')
    app.register_blueprint(sync_bp, url_prefix='/api/sync')

    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'message': 'Secure E-Voting Backend API is running'
        }), 200

    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'name': 'Secure E-Voting System API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'admin': '/api/admin',
                'sign': '/api/sign',
                'voice': '/api/voice',
                'sync': '/api/sync',
                'health': '/health'
            }
        }), 200

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500

    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

    return app


if __name__ == '__main__':
    app = create_app()

    # Get port from environment or default to 8000
    port = int(os.getenv('PORT', 8000))

    print(f"""
    ╔═══════════════════════════════════════════════════════╗
    ║   Secure E-Voting System - Backend API Server       ║
    ║   Version: 1.0.0                                     ║
    ║   Running on: http://localhost:{port}                  ║
    ╚═══════════════════════════════════════════════════════╝

    API Endpoints:
    - POST   /api/auth/register              - Register new voter
    - POST   /api/auth/register-face         - Register face biometrics
    - POST   /api/auth/login/request-otp     - Request OTP for login
    - POST   /api/auth/login/verify          - Verify OTP and face
    - GET    /api/auth/voter/<wallet>        - Get voter info

    Admin Endpoints:
    - GET    /api/admin/voters               - Get all voters
    - GET    /api/admin/voters/stats         - Get voter statistics
    - GET    /api/admin/audit-logs           - Get audit logs
    - GET    /api/admin/alerts               - Get security alerts
    - POST   /api/admin/alerts/<id>/resolve  - Resolve alert
    - POST   /api/admin/voters/<id>/unlock   - Unlock account
    - DELETE /api/admin/voters/<id>          - Delete voter

    Sign Language Voting Endpoints:
    - GET    /api/sign/candidates            - Get all candidates with sign numbers
    - GET    /api/sign/candidates/<sign>     - Get candidate by sign number
    - POST   /api/sign/detect                - Detect sign from image
    - POST   /api/sign/vote                  - Cast vote using sign language
    - GET    /api/sign/stats                 - Get voting statistics

    Voice Voting Endpoints:
    - GET    /api/voice/candidates           - Get all candidates for voice voting
    - POST   /api/voice/recognize            - Recognize voice and match candidate
    - POST   /api/voice/vote                 - Cast vote using voice

    Blockchain Sync Endpoints:
    - POST   /api/sync/candidates            - Sync candidates from blockchain to database
    - GET    /api/sync/status                - Check sync status

    Press CTRL+C to stop the server
    """)

    app.run(host='0.0.0.0', port=port, debug=True)