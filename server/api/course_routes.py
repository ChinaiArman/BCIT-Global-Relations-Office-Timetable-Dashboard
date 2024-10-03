"""
"""

# IMPORTS
from flask import Blueprint, jsonify


# DEFINE BLUEPRINT
course_bp = Blueprint('course_bp', __name__)


# ROUTES
@course_bp.route('/course/<int:id>/', methods=['GET'])
def get_course_by_id(id):
    return jsonify({"message": f"course {id} endpoint"})

@course_bp.route('/course/<str:course_code>/', methods=['GET'])
def get_course_by_code(course_code):
    return jsonify({"message": f"course {course_code} endpoint"})

@course_bp.route('/course/', methods=['POST'])
def create_course():
    return jsonify({"message": "course create endpoint"})

@course_bp.route('/course/<int:id>/', methods=['PUT'])
def update_course(id):
    return jsonify({"message": f"course {id} update endpoint"})

@course_bp.route('/course/<int:id>/', methods=['DELETE'])
def delete_course(id):
    return jsonify({"message": f"course {id} delete endpoint"})

@course_bp.route('/course/import', methods=['POST'])
def upload_course():
    return jsonify({"message": "course upload endpoint"})

@course_bp.route('/course/export', methods=['GET'])
def download_course():
    return jsonify({"message": "course export endpoint"})

@course_bp.route('/course/<int:id>/students/', methods=['GET'])
def get_course_students(id):
    return jsonify({"message": f"course {id} students endpoint"})

@course_bp.route('/course/download_template', methods=['GET'])
def download_template():
    return jsonify({"message": "course download template endpoint"})
