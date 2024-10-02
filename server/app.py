"""
"""

# IMPORTS
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os


# ENVIRONMENT VARIABLES
load_dotenv()
PORT = os.getenv('PORT', 5000)


# FLASK CONFIGURATION
app = Flask(__name__)
CORS(app)


# ROUTES
@app.route('/', methods=['GET'])
def get():
    return jsonify({'message': 'Hello World!'})


# MAIN
if __name__ == '__main__':
    app.run(debug=True)
