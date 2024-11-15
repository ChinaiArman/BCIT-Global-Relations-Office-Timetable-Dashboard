"""
This module defines the routes for course-related operations within the BCIT Global Relations Office Timetable Dashboard server.
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app

from services.decorators import verified_login_required


# DEFINE BLUEPRINT
course_bp = Blueprint('course_bp', __name__)


# ROUTES
@course_bp.route('/course/get-all-course-groupings-by-course-code/<string:course_code>/<string:student_id>', methods=['GET'])
@verified_login_required
def get_all_course_groupings_by_course_code(course_code, student_id):
    """
    """
    try:
        db = current_app.config['database']
        response = db.get_all_course_groupings_by_course_code(course_code, student_id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

    
@course_bp.route('/course/course_grouping/<string:course_grouping>/', methods=['GET'])
@verified_login_required
def get_course_by_course_grouping(course_grouping):
    """
    Request: GET /course/course_grouping/<string:course_grouping>/

    Description: Retrieve courses by their course grouping.

    Parameters:
    - course_grouping (string): The course grouping.

    Response:
    - courses (list): A list of courses matching the course grouping.

    Status Codes:
    - 200: Course data successfully retrieved.
    - 404: Course not found.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config['database']
        response = db.get_course_by_course_grouping(course_grouping)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@course_bp.route('/course/course_id/<string:id>/', methods=['GET'])
@verified_login_required
def get_course_by_id(id):
    """
    Request: GET /course/course_id/<string:id>/

    Description: Retrieve a course by its ID.

    Parameters:
    - id (string): The course ID.

    Response:
    - course (object): The course matching the ID.

    Status Codes:
    - 200: Course data successfully retrieved.
    - 404: Course not found.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config['database']
        response = db.get_course_by_course_id(id)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@course_bp.route('/course/import', methods=['PUT'])
# @verified_login_required
def upload_course():
    """
    Request: PUT /course/import

    Description: Upload a XLSX file to the MYSQL Database containing course data.

    Request Body:
    - file: XLSX file containing course data.

    Response:
    - message: Success or error message.

    Status Codes:
    - 201: Course data successfully uploaded.
    - 400: Invalid request.
    - 500: Internal server error.

    Author: ``@ChinaiArman``
    """
    try:
        db = current_app.config['database']
        response = db.bulk_course_upload(request.files['file'])
        return jsonify({"message": "Course data successfully uploaded", "invalid_rows": response }), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@course_bp.route('/course/export', methods=['GET'])
@verified_login_required
def download_course():
    """
    """
    return jsonify({"message": "course export endpoint"})

@course_bp.route('/course/<string:course_grouping>/students/', methods=['GET'])
@verified_login_required
def get_course_students(course_grouping):
    """
    Request: GET /course/<string:course_grouping>/students/

    Description: Retrieve a list of students enrolled in a specific course.

    Parameters:
    - course_grouping (string): The course grouping.

    Response:
    - list: A list of student objects.

    Status Codes:
    - 200: Students retrieved successfully.
    - 404: Course not found.

    Author: Kate Sullivan
    """
    try:
        db = current_app.config['database']
        response = db.get_course_students(course_grouping)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 404

@course_bp.route('/course/download_template', methods=['GET'])
@verified_login_required
def download_template():
    """
    """
    return jsonify({"message": "course download template endpoint"})
    