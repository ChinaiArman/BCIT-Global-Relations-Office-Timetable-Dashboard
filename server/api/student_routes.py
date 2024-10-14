"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app


# DEFINE BLUEPRINT
student_bp = Blueprint("student_bp", __name__)


# ROUTES
@student_bp.route("/student/<string:id>/", methods=["GET"])
def get_student_by_id(id):
    """ """
    try:
        db = current_app.config["database"]
        response = db.get_student_by_id(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/", methods=["POST"])
def create_student():
    """ """
    try:
        data = request.get_json()
        db = current_app.config["database"]
        db.create_student(data)
        return jsonify({"message": "Student created successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/<string:id>/", methods=["PUT"])
def update_student(id):
    """ """
    try:
        db = current_app.config["database"]
        data = request.get_json()
        db.update_student(id, data)
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/<string:id>/", methods=["DELETE"])
def delete_student(id):
    """ """
    try:
        db = current_app.config["database"]
        db.delete_student(id)
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/import", methods=["PUT"])
def upload_student():
    """ """
    try:
        db = current_app.config["database"]
        response = db.bulk_student_upload(request.files["file"])
        return jsonify({"message": "Student data successfully uploaded", "invalid_rows": response}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/export", methods=["GET"])
def download_student():
    """ """
    return jsonify({"message": "student export endpoint"})


@student_bp.route("/student/<string:id>/courses/", methods=["GET"])
def get_student_courses(id):
    """ """
    try:
        db = current_app.config["database"]
        response = db.get_student_courses(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/download_template", methods=["GET"])
def download_template():
    """ """
    return jsonify({"message": "student download template endpoint"})
