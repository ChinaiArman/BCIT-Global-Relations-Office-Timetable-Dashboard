"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app


# DEFINE BLUEPRINT
authentication_bp = Blueprint('authentication_bp', __name__)


# ROUTES
@authentication_bp.route('/authenticate/login/', methods=['POST'])
def login():
    """
    """
    return jsonify({"message": "login endpoint"})

@authentication_bp.route('/authenticate/logout/', methods=['POST'])
def logout():
    """
    """
    return jsonify({"message": "logout endpoint"})

@authentication_bp.route('/authenticate/register/', methods=['POST'])
def register():
    """
    """
    return jsonify({"message": "register endpoint"})

@authentication_bp.route('/authenticate/reset_password/', methods=['POST'])
def reset_password():
    """
    """
    return jsonify({"message": "reset password endpoint"})

@authentication_bp.route('/authenticate/verify/', methods=['POST'])
def verify():
    """
    """
    return jsonify({"message": "verify endpoint"})
