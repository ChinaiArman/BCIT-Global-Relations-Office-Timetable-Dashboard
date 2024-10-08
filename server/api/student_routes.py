"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app


# INSTANTIATE SERVICES


# DEFINE BLUEPRINT
student_bp = Blueprint('student_bp', __name__)


# ROUTES
@student_bp.route('/student/<int:id>/', methods=['GET'])
def get_student_by_id(id):
    """
    """
    return jsonify({"message": f"student {id} endpoint"})

@student_bp.route('/student/', methods=['POST'])
def create_student():
    """
    """
    return jsonify({"message": "student create endpoint"})

@student_bp.route('/student/<int:id>/', methods=['PUT'])
def update_student(id):
    """
    """
    return jsonify({"message": f"student {id} update endpoint"})

@student_bp.route('/student/<int:id>/', methods=['DELETE'])
def delete_student(id):
    """
    """
    return jsonify({"message": f"student {id} delete endpoint"})

@student_bp.route('/student/import', methods=['PUT'])
def upload_student():
    """
    """
    db = current_app.config['database']
    try:
        response = db.bulk_student_upload(request.files['file'])
        return jsonify({"message": "Student data successfully uploaded", "invalid_rows": response }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route('/student/export', methods=['GET'])
def download_student():
    """
    """
    return jsonify({"message": "student export endpoint"})

@student_bp.route('/student/<int:id>/courses/', methods=['GET'])
def get_student_courses(id):
    """
    """
    return jsonify({"message": f"student {id} courses endpoint"})

@student_bp.route('/student/download_template', methods=['GET'])
def download_template():
    """
    """
    return jsonify({"message": "student download template endpoint"})
