from flask import Blueprint, jsonify, request, current_app, session

from services.decorators import verified_login_required


# DEFINE BLUEPRINT
database_bp = Blueprint('database_bp', __name__)


# ROUTES
@database_bp.route('/database/jumbotron', methods=['GET'])
def get_jumbotron_data():
    """
    """
    try:
        db = current_app.config['database']
        response = db.get_jumbotron_data()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

@database_bp.route('/database/schedule-progression', methods=['GET'])
def get_schedule_progression():
    """
    """
    try:
        db = current_app.config['database']
        response = db.get_schedule_progression()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
@database_bp.route('/database/most-popular-preferences', methods=['GET'])
def get_most_popular_preferences():
    """
    """
    try:
        db = current_app.config['database']
        response = db.get_most_popular_preferences()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
@database_bp.route('/database/most-popular-course-registrations', methods=['GET'])
def get_most_popular_course_registrations():
    """
    """
    try:
        db = current_app.config['database']
        response = db.get_most_popular_course_registrations()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500