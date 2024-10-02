"""
"""

# IMPORTS
from flask import Blueprint, jsonify


# DEFINE BLUEPRINT
course_bp = Blueprint('course_bp', __name__)


# ROUTES
@course_bp.route('/course/', methods=['GET'])
def get_course():
    return jsonify({"message": "course root endpoint"})