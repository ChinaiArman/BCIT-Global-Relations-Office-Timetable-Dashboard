"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app


# INSTANTIATE SERVICES
from services.Database import Database
from models.Student import Student

# DEFINE BLUEPRINT
student_bp = Blueprint("student_bp", __name__)


# ROUTES
@student_bp.route("/students/<int:id>/", methods=["GET"])
def get_student_by_id(id):
    db = current_app.config["database"]
    response = db.get_student_by_id(id)
    return (
        jsonify({"message": response["message"], "data": response["data"]}),
        response["status"],
    )


@student_bp.route("/students/", methods=["POST"])
def create_student():
    """ """
    data = request.get_json()
    # Need to match the keys of the data with the Student parameters
    student = Student(**data)
    db = current_app.config["database"]
    response = db.create_student(student)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/students/<int:id>/", methods=["PUT"])
def update_student(id):
    """ """
    db = current_app.config["database"]
    data = request.get_json()
    response = db.update_student(id, data)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/students/<int:id>/", methods=["DELETE"])
def delete_student(id):
    """ """
    db = current_app.config["database"]
    response = db.delete_student(id)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/students/import", methods=["PUT"])
def upload_students():
    """ """
    return jsonify({"message": "student import endpoint"})


@student_bp.route("/students/export", methods=["GET"])
def download_students():
    """ """
    return jsonify({"message": "student export endpoint"})


@student_bp.route("/students/<int:id>/courses/", methods=["GET"])
def get_student_courses(id):
    """ """
    db = current_app.config["database"]
    response = db.get_student_courses(id)
    return (
        jsonify({"message": response["message"], "data": response["data"]}),
        response["status"],
    )


@student_bp.route("/students/download_template", methods=["GET"])
def download_template():
    """ """
    db = current_app.config["database"]
    response = db.download_student_template()
    return jsonify({"message": "student download template endpoint"})
