"""
"""

# IMPORTS
from flask import Flask, jsonify
from flask_cors import CORS

from api.student_routes import student_bp
from api.course_routes import course_bp
from api.schedule_routes import schedule_bp
from api.authentication_routes import authentication_bp

from services.Database import Database
from services.Authenticator import Authenticator
from services.Scheduler import Scheduler
from services.EmailManager import EmailManager

from db_config import db, configure_db
from session_config import configure_sessions
from logging_config import configure_logging


# FLASK CONFIGURATION
def create_app():
    app = Flask(__name__)
    CORS(app)

    # DATABASE CONFIGURATION
    configure_db(app)

    # SESSION CONFIGURATION
    configure_sessions(app, db)

    # LOGGING CONFIGURATION
    configure_logging(app)

    # CONFIGURE SERVICES
    app.config['database'] = Database(db)
    app.config['authenticator'] = Authenticator()
    app.config['studentManager'] = Scheduler()
    app.config['emailManager'] = EmailManager()


    # ROUTES
    @app.route('/', methods=['GET'])
    def _():
        return jsonify({"message": "Hello World"})

    app.register_blueprint(student_bp, url_prefix='/api')
    app.register_blueprint(course_bp, url_prefix='/api')
    app.register_blueprint(schedule_bp, url_prefix='/api')
    app.register_blueprint(authentication_bp, url_prefix='/api')
