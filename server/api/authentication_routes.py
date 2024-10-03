"""
"""

# IMPORTS
from flask import Blueprint, jsonify


# DEFINE BLUEPRINT
authentication_bp = Blueprint('authentication_bp', __name__)


# ROUTES
@authentication_bp.route('/login/', methods=['POST'])
def login():
    return jsonify({"message": "login endpoint"})

@authentication_bp.route('/logout/', methods=['POST'])
def logout():
    return jsonify({"message": "logout endpoint"})

@authentication_bp.route('/register/', methods=['POST'])
def register():
    return jsonify({"message": "register endpoint"})

@authentication_bp.route('/reset_password/', methods=['POST'])
def reset_password():
    return jsonify({"message": "reset password endpoint"})

@authentication_bp.route('/change_password/', methods=['POST'])
def change_password():
    return jsonify({"message": "change password endpoint"})
