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
from logging_config import configure_logging
from dotenv import load_dotenv
import os


# FLASK CONFIGURATION
def create_app():
    """
    """

    load_dotenv()

    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:3001", "allow_headers": ["Content-Type"]}}, supports_credentials=True)

    # CONFIGURE SERVICES
    app.config['database'] = Database(db)
    app.config['authenticator'] = Authenticator()
    app.config['studentManager'] = Scheduler()
    app.config['email_manager'] = EmailManager(
        gmail_user=os.getenv('GMAIL_EMAIL'),
        gmail_password=os.getenv('GMAIL_PASSWORD'),
        base_url=os.getenv('BASE_URL')
    )

    # DATABASE CONFIGURATION
    configure_db(app)

    # SESSION CONFIGURATION
    configure_sessions(app, db)

    # LOGGING CONFIGURATION
    # configure_logging(app)

    


    # ROUTES
    @app.route('/', methods=['GET'])
    def _():
        return jsonify({"message": "Hello World"})
    
    # set response headers
    @app.after_request
    def _(response):
        # if OPTIONS request, return response right away
        if request.method == 'OPTIONS':
            # set response headers
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3001'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            return response
        # set response headers
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3001'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
            

    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')
    app.register_blueprint(authentication_bp, url_prefix='/api')
    app.register_blueprint(email_bp, url_prefix='/api')
    app.register_blueprint(database_bp, url_prefix='/api')
    return app, db