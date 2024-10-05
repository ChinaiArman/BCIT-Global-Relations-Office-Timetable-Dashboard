"""
"""

# IMPORTS
from flask import Flask, jsonify, request, g
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
from services.StudentManager import StudentManager
from services.CourseManager import CourseManager
from services.EmailManager import EmailManager


# ENVIRONMENT VARIABLES
load_dotenv()
PORT = os.getenv('PORT', 5000)


# FLASK CONFIGURATION
app = Flask(__name__)
CORS(app)


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
app.config['database'] = Database()
app.config['authenticator'] = Authenticator()
app.config['studentManager'] = StudentManager()
app.config['courseManager'] = CourseManager()
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
    app.run(debug=True)
