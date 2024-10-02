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

@course_bp.route('/course/<int:id>/', methods=['GET'])
def get_course_by_id(id):
    return jsonify({"message": f"course {id} endpoint"})

@course_bp.route('/course/', methods=['POST'])
def create_course():
    return jsonify({"message": "course create endpoint"})

@course_bp.route('/course/<int:id>/', methods=['PUT'])
def update_course(id):
    return jsonify({"message": f"course {id} update endpoint"})

@course_bp.route('/course/<int:id>/', methods=['DELETE'])
def delete_course(id):
    return jsonify({"message": f"course {id} delete endpoint"})

@course_bp.route('/course/upload_xlsx', methods=['POST'])
def upload_course():
    return jsonify({"message": "course upload xlsx endpoint"})

@course_bp.route('/course/download_xlsx', methods=['GET'])
def download_course():
    return jsonify({"message": "course download xlsx endpoint"})
