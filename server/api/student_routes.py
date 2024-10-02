"""
"""

# IMPORTS
from flask import Blueprint, jsonify


# DEFINE BLUEPRINT
student_bp = Blueprint('student_bp', __name__)


# ROUTES
@student_bp.route('/students/', methods=['GET'])
def get_students():
    return jsonify({"message": "student root endpoint"})