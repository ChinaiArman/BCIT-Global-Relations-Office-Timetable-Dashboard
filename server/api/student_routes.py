"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app, send_file

from services.decorators import verified_login_required


# DEFINE BLUEPRINT
student_bp = Blueprint("student_bp", __name__)


# ROUTES
@student_bp.route("/student/<string:id>/", methods=["GET"])
@verified_login_required
def get_student_by_id(id):
    """
    Request: GET /student/<string:id>/

    Description: Retrieve a student by their ID.

    Parameters:
    - id (string): The student ID.

    Response:
    - student (object): The student matching the ID.

    Status Codes:
    - 200: Student data successfully retrieved.
    - 404: Student not found.
    - 500: Internal server error.

    Author: Lex Wong
    """
    try:
        db = current_app.config["database"]
        response = db.get_student_by_id(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/", methods=["POST"])
@verified_login_required
def create_student():
    """
    Request: POST /student/

    Description: Create a new student.

    Request Body:
    - data (object): The student data to be created.

    Response:
    - message (string): The response message indicating success or failure.

    Status Codes:
    - 200: Student created successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: Lex Wong
    """
    try:
        data = request.get_json()
        db = current_app.config["database"]
        db.create_student(data)
        return jsonify({"message": "Student created successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/<string:id>/", methods=["PUT"])
@verified_login_required
def update_student(id):
    """
    Request: PUT /student/<string:id>/

    Description: Update a student's information.

    Parameters:
    - id (string): The student ID.
    - data (object): The updated student data.

    Response:
    - message (string): The response message indicating success or failure.

    Status Codes:
    - 200: Student updated successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: Lex Wong
    """
    try:
        db = current_app.config["database"]
        data = request.get_json()
        db.update_student(id, data)
        return jsonify({"message": "Student updated successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@student_bp.route("/student/<string:id>/", methods=["DELETE"])
@verified_login_required
def delete_student(id):
    """
    Request: DELETE /student/<string:id>/

    Description: Delete a student's information.

    Parameters:
    - id (string): The student ID.

    Response:
    - message (string): The response message indicating success or failure.

    Status Codes:
    - 200: Student deleted successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: Charlie Zhang
    """
    try:
        db = current_app.config["database"]
        db.delete_student(id)
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/import", methods=["PUT"])
@verified_login_required
def upload_student():
    """
    Request: PUT /student/import

    Description: Upload a CSV file to import student data.

    Request Body:
    - file: The CSV file containing student data.

    Response:
    - message: Success or error message.
    - invalid_rows: List of rows that failed to upload due to errors.

    Status Codes:
    - 201: Student data successfully uploaded.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: Charlie Zhang
    """
    try:
        db = current_app.config["database"]
        response = db.bulk_student_upload(request.files["file"])
        return jsonify({"message": "Student data successfully uploaded", "invalid_rows": response}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/get_all", methods=["GET"])
@verified_login_required
def get_all_students():
    """
    Request: GET /student/get_all

    Description: Retrieve all students.

    Response:
    - students (list): A list of all students.

    Status Codes:
    - 200: Student data successfully retrieved.
    - 500: Internal server error.

    Author: Charlie Zhang
    """
    try:
        db = current_app.config["database"]
        response = db.get_all_students()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/export", methods=["GET"])
@verified_login_required
def download_student():
    """
    Request: GET /student/export/

    Description: Export student data as a CSV file.

    Response:
    - file: The CSV file containing student data.

    Status Codes:
    - 200: Student data successfully exported.
    - 400: Invalid request.

    Author: ``@ArmanChinai``
    """
    try:
        db = current_app.config["database"]
        file_path = db.export_student()
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/download_template", methods=["GET"])
@verified_login_required
def download_template():
    """
    Request: GET /student/download_template/

    Description: Download the student upload template.

    Response:
    - file: The student upload template file.

    Status Codes:
    - 200: Template successfully downloaded.
    - 400: Invalid request.

    Author: ``@ArmanChinai``
    """
    try:
        return send_file("templates/student_upload_template.csv", as_attachment=True)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/add_course/student/<string:student_id>/course/<string:course_id>/", methods=["PUT"])
@verified_login_required
def add_course_to_student_route(student_id, course_id):
    """
    Request: PUT /student/add_course/student/<string:student_id>/course/<string:course_id>/

    Description: Add a course to a student.

    Parameters:
    - student_id (string): The student ID.
    - course_id (string): The course ID.

    Response:
    - message: Success or error message.

    Status Codes:
    - 200: Course added successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config["database"]
        db.add_course_to_student(student_id, course_id)
        return jsonify({"message": "Course added successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/remove_course/student/<string:student_id>/course/<string:course_id>/", methods=["PUT"])
@verified_login_required
def remove_course_from_student_route(student_id, course_id):
    """
    Request: PUT /student/remove_course/student/<string:student_id>/course/<string:course_id>/

    Description: Remove a course from a student.

    Parameters:
    - student_id (string): The student ID.
    - course_id (string): The course ID.

    Response:
    - message: Success or error message.

    Status Codes:
    - 200: Course removed successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config["database"]
        db.remove_course_from_student(student_id, course_id)
        return jsonify({"message": "Course removed successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/replace_all_courses/student/<string:student_id>/course_list/<string:course_list>", methods=["PUT"])
@verified_login_required
def replace_all_courses_for_student_route(student_id, course_list):
    """
    Request: PUT /student/replace_all_courses/student/<string:student_id>/course_list/<string:course_list>

    Description: Replace all courses for a student.

    Parameters:
    - student_id (string): The student ID.
    - course_list (string): The comma-separated list of course IDs.

    Response:
    - message: Success or error message.

    Status Codes:
    - 200: Courses replaced successfully.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config["database"]
        db.replace_all_courses_for_student(student_id, course_list)
        return jsonify({"message": "Courses replaced successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400

