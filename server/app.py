"""
"""

# IMPORTS
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from api.student_routes import student_bp
from api.course_routes import course_bp
from api.schedule_routes import schedule_bp
from api.authentication_routes import authentication_bp


# ENVIRONMENT VARIABLES
load_dotenv()
PORT = os.getenv('PORT', 5000)


# FLASK CONFIGURATION
app = Flask(__name__)
CORS(app)


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
