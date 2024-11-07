"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app

from services.decorators import verified_login_required


# DEFINE BLUEPRINT
schedule_bp = Blueprint('schedule_bp', __name__)


# ROUTES
@schedule_bp.route('/schedule/<int:id>/', methods=['GET'])
@verified_login_required
def get_schedule_by_id(id):
    """
    """
    return jsonify({"message": f"schedule {id} endpoint"})

@schedule_bp.route('/schedule/', methods=['POST'])
@verified_login_required
def create_schedule():
    """
    """
    return jsonify({"message": "schedule create endpoint"})

@schedule_bp.route('/schedule/<int:id>/', methods=['PUT'])
@verified_login_required
def update_schedule(id):
    """
    """
    return jsonify({"message": f"schedule {id} update endpoint"})

@schedule_bp.route('/schedule/<int:id>/', methods=['DELETE'])
@verified_login_required
def delete_schedule(id):
    """
    """
    return jsonify({"message": f"schedule {id} delete endpoint"})

@schedule_bp.route('/schedule/download', methods=['POST'])
@verified_login_required
def download_schedules():
    """
    """
    return jsonify({"message": "schedule download endpoint"})
