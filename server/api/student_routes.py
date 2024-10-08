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
@student_bp.route("/student/<string:id>/", methods=["GET"])
def get_student_by_id(id):
    """ """
    db = current_app.config["database"]
    response = db.get_student_by_id(id)
    return (
        jsonify({"message": response["message"], "data": response["data"]}),
        response["status"],
    )


@student_bp.route("/student/", methods=["POST"])
def create_student():
    """ """
    data = request.get_json()
    db = current_app.config["database"]
    response = db.create_student(data)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/student/<string:id>/", methods=["PUT"])
def update_student(id):
    """ """
    db = current_app.config["database"]
    data = request.get_json()
    response = db.update_student(id, data)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/student/<string:id>/", methods=["DELETE"])
def delete_student(id):
    """ """
    db = current_app.config["database"]
    response = db.delete_student(id)
    return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/student/import", methods=["PUT"])
def upload_student():
    """ """
    db = current_app.config["database"]
    try:
        response = db.bulk_student_upload(request.files["file"])
        return (
            jsonify(
                {
                    "message": "Student data successfully uploaded",
                    "invalid_rows": response,
                }
            ),
            201,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/export", methods=["GET"])
def download_student():
    """ """
    return jsonify({"message": "student export endpoint"})


@student_bp.route("/student/<string:id>/courses/", methods=["GET"])
def get_student_courses(id):
    """ """
    db = current_app.config["database"]
    response = db.get_student_courses(id)
    if response["status"] == 200 or response["status"] == 500:
        return (
            jsonify({"message": response["message"], "data": response["data"]}),
            response["status"],
        )
    else:
        return jsonify({"message": response["message"]}), response["status"]


@student_bp.route("/student/download_template", methods=["GET"])
def download_template():
    """ """
    db = current_app.config["database"]
    response = db.download_student_template()
    return jsonify({"message": "student download template endpoint"})
