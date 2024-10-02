"""
"""

# IMPORTS
from flask import Blueprint, jsonify


# DEFINE BLUEPRINT
schedule_bp = Blueprint('schedule_bp', __name__)


# ROUTES
@schedule_bp.route('/schedule/', methods=['GET'])
def get_schedules():
    return jsonify({"message": "schedule root endpoint"})