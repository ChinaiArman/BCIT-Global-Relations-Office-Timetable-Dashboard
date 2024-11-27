"""
"""

# IMPORTS
from flask import Flask, jsonify, request
from flask_cors import CORS

from api.student_routes import student_bp
from api.course_routes import course_bp
from api.schedule_routes import schedule_bp
from api.authentication_routes import authentication_bp
from api.email_routes import email_bp
from api.database_routes import database_bp

from services.Database import Database
from services.Authenticator import Authenticator
from services.Scheduler import Scheduler
from services.EmailManager import EmailManager

from db_config import db, configure_db
from session_config import configure_sessions
from dotenv import load_dotenv
import os


# CONSTANTS
load_dotenv()
CLIENT_URL = os.getenv('CLIENT_URL')


# FLASK CONFIGURATION
def create_app():
    """
    """

    load_dotenv()

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": CLIENT_URL, "allow_headers": ["Content-Type"]}}, supports_credentials=True)

    # CONFIGURE SERVICES
    app.config['database'] = Database(db)
    app.config['authenticator'] = Authenticator()
    app.config['studentManager'] = Scheduler()
    app.config['email_manager'] = EmailManager(
        gmail_user=os.getenv('GMAIL_EMAIL'),
        gmail_password=os.getenv('GMAIL_PASSWORD'),
        client_url=CLIENT_URL
    )

    # DATABASE CONFIGURATION
    configure_db(app)

    # SESSION CONFIGURATION
    configure_sessions(app, db)

    
    # ROUTES
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({"message": "Hello World"})
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "OK"}), 200
    
    # RESPONSE HEADERS
    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = CLIENT_URL
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        # Handle OPTIONS request directly
        if request.method == 'OPTIONS':
            response.status_code = 200
        return response
            
    # REGISTER BLUEPRINTS
    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')
    app.register_blueprint(authentication_bp, url_prefix='/api')
    app.register_blueprint(email_bp, url_prefix='/api')
    app.register_blueprint(database_bp, url_prefix='/api')
    return app, db
