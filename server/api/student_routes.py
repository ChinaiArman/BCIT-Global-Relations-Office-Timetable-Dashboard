"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app, send_file

from services.decorators import verified_login_required
import os


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
def bulk_replace_student():
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
        response = db.bulk_student_replace(request.files["file"])
        return jsonify({"message": "Student data successfully uploaded", "results": response}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@student_bp.route("/student/import", methods=["PATCH"])
@verified_login_required
def bulk_update_student():
    """
    """
    try:
        db = current_app.config["database"]
        response = db.bulk_student_update(request.files["file"])
        return jsonify({"message": "Student data successfully updated", "results": response}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@student_bp.route("/student/get-all", methods=["GET"])
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
        file_path = os.path.join(current_app.root_path, 'resources/templates/student_upload_template.csv')
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@student_bp.route("/student/replace-course-groupings/<string:student_id>", methods=["PUT"])
@verified_login_required
def replace_courses_with_new_course_groupings(student_id):
    """
    """
    try:
        db = current_app.config["database"]
        data = request.get_json()
        db.remove_all_course_groupings(student_id)
        db.add_courses_by_groupings(student_id, data["course_groupings"])
        return jsonify({"message": "Course groupings added to student successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    

@student_bp.route("/student/flip-mark-done/<string:student_id>", methods=["POST"])
@verified_login_required
def flip_mark_student_done(student_id):
    """
    Request: POST /student/mark-done/<string:student_id

    Description: Mark a student as done.

    Parameters:
    - student_id (string): The student ID.

    Response:
    - message: Success or error message.

    Status Codes:
    - 200: Student marked as done.
    - 400: Invalid request.
    - 500: Internal server error.
    """
    try:
        db = current_app.config["database"]
        db.flip_mark_done(student_id)
        return jsonify({"message": "Student marked as done"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    

@student_bp.route("/student/flip-department-approval/<string:student_id>", methods=["POST"])
@verified_login_required
def flip_department_approval(student_id):
    """
    """
    try:
        db = current_app.config["database"]
        db.flip_program_head_approval(student_id)
        return jsonify({"message": "Student marked as done"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400