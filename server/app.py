"""
"""

# IMPORTS
from flask import Flask, jsonify, request, g
from flask_sqlalchemy import SQLAlchemy
import time
from flask_cors import CORS
from dotenv import load_dotenv
import os

from logging_config import configure_logging

from api.student_routes import student_bp
from api.course_routes import course_bp
from api.schedule_routes import schedule_bp
from api.authentication_routes import authentication_bp

from services.Database import Database
from services.Authenticator import Authenticator
from services.Scheduler import Scheduler
from services.EmailManager import EmailManager

from db_config import db


# ENVIRONMENT VARIABLES
load_dotenv()
PORT = os.getenv('PORT', 5000)
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


# FLASK CONFIGURATION
app = Flask(__name__)
CORS(app)


# DATABASE CONFIGURATION
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# LOGGING CONFIGURATION
configure_logging(app)
@app.before_request
def log_request():
    g.start_time = time.time()
    app.logger.info(f"Incoming request Request: {request.method} {request.path}")

@app.after_request
def log_response(response):
    execution_time = time.time() - g.start_time
    app.logger.info(f"Completed request: {request.method} {request.path} "f"with status {response.status_code} in {execution_time:.4f}s")
    return response

@app.teardown_request
def log_request_teardown(error=None):
    if error is not None:
        app.logger.error(f"An error occurred: {error}")


# CONFIGURE SERVICES
app.config['database'] = Database(db)
app.config['authenticator'] = Authenticator()
app.config['studentManager'] = Scheduler()
app.config['emailManager'] = EmailManager()


# ROUTES
@app.route('/', methods=['GET'])
def root():
    return jsonify({"message": "Hello World"})

app.register_blueprint(student_bp, url_prefix='/api')
app.register_blueprint(course_bp, url_prefix='/api')
app.register_blueprint(schedule_bp, url_prefix='/api')
app.register_blueprint(authentication_bp, url_prefix='/api')


# MAIN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
