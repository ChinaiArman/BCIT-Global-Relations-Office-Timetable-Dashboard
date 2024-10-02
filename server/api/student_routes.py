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

@student_bp.route('/students/<int:id>/', methods=['GET'])
def get_student_by_id(id):
    return jsonify({"message": f"student {id} endpoint"})

@student_bp.route('/students/', methods=['POST'])
def create_student():
    return jsonify({"message": "student create endpoint"})

@student_bp.route('/students/<int:id>/', methods=['PUT'])
def update_student(id):
    return jsonify({"message": f"student {id} update endpoint"})

@student_bp.route('/students/<int:id>/', methods=['DELETE'])
def delete_student(id):
    return jsonify({"message": f"student {id} delete endpoint"})

@student_bp.route('/students/upload_xlsx', methods=['POST'])
def upload_student():
    return jsonify({"message": "student upload xlsx endpoint"})

@student_bp.route('/students/download_xlsx', methods=['GET'])
def download_student():
    return jsonify({"message": "student download xlsx endpoint"})

@student_bp.route('/students/<int:id>/courses/', methods=['GET'])
def get_student_courses(id):
    return jsonify({"message": f"student {id} courses endpoint"})

@student_bp.route('/students/<int:id>/schedules/', methods=['GET'])
def get_student_schedules(id):
    return jsonify({"message": f"student {id} schedules endpoint"})
