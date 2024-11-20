"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app, send_file
import os

from services.decorators import verified_login_required


# DEFINE BLUEPRINT
schedule_bp = Blueprint('schedule_bp', __name__)


# ROUTES
@schedule_bp.route('/schedule/export', methods=['GET'])
@verified_login_required
def download_schedules():
    """
    """
    try:
        db = current_app.config['database']
        file_path = db.save_schedules_to_local_file()
        return send_file(file_path, as_attachment=True), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400
