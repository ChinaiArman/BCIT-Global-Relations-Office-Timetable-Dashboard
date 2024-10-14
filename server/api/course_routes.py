"""
This module defines the routes for course-related operations within the BCIT Global Relations Office Timetable Dashboard server.
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app


# DEFINE BLUEPRINT
course_bp = Blueprint('course_bp', __name__)


# ROUTES
@course_bp.route('/course/<int:crn>/', methods=['GET'])
def get_course_by_crn(crn):
    """
    Request: GET /course/<int:crn>/

    Description: Retrieve a course by its CRN.

    Parameters:
    - crn (int): The Course Registration Number.

    Response:
    - courses (list): A list of courses matching the CRN.

    Status Codes:
    - 200: Course data successfully retrieved.
    - 404: Course not found.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config['database']
        response = db.get_course_by_crn(crn)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@course_bp.route('/course/block/<string:block>/course_code/<string:course_code>/', methods=['GET'])
def get_course_by_block_and_course_code(block, course_code):
    """
    Request: GET /course/block/<string:block>/course_code/<string:course_code>/

    Description: Retrieve a course by its block and course code.

    Parameters:
    - block (string): The block of the course.
    - course_code (string): The course code.

    Response:
    - courses (list): A list of courses matching the block and course code.

    Status Codes:
    - 200: Course data successfully retrieved.
    - 404: Course not found.
    - 500: Internal server error.

    Author: ``@KateSullivan``
    """
    try:
        db = current_app.config['database']
        response = db.get_courses_by_block_and_course_code(block, course_code)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



@course_bp.route('/course/import', methods=['PUT'])
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
def download_course():
    """
    """
    return jsonify({"message": "course export endpoint"})

@course_bp.route('/course/<string:block>/<string:course_code>/students/', methods=['GET'])
def get_course_students(block, course_code):
    """
    Request: GET /course/<string:block>/<string:course_code>/students/

    Description: Retrieve a list of students enrolled in a specific course.

    Parameters:
    - block (string): The block of the course.
    - course_code (string): The code of the course.

    Response:
    - list: A list of student objects.

    Status Codes:
    - 200: Students retrieved successfully.
    - 404: Course not found.

    Author: Kate Sullivan
    """
    # course = Course.query.filter_by(block=block, course_code=course_code).first()
    # if course:
    #     students = [student.serialize() for student in course.students]
    #     return jsonify(students)
    # else:
    #     return jsonify({"message": "Course not found"}), 404
    return jsonify({"message": "get course students endpoint"})

@course_bp.route('/course/download_template', methods=['GET'])
def download_template():
    """
    """
    return jsonify({"message": "course download template endpoint"})
