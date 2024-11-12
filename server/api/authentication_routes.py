"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app, session

from services.decorators import verified_login_required, admin_required, unverified_login_required


# DEFINE BLUEPRINT
authentication_bp = Blueprint('authentication_bp', __name__)


# ROUTES
@authentication_bp.route('/authenticate/login/', methods=['POST'])
def login() -> tuple:
    """
    Login a user.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        db = current_app.config['database']
        authenticator = current_app.config['authenticator']
        email = request.json.get('email')
        password = request.json.get('password')
        user = db.get_user_by_email(email)
        authenticator.verify_password(password, user.password)
        session.permanent = True
        session["user_id"] = user.id
        return jsonify({"message": "login successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/logout/', methods=['POST'])
@verified_login_required
def logout() -> tuple:
    """
    Logout a user.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        session.clear()
        return jsonify({"message": "logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# @authentication_bp.route('/authenticate/register/', methods=['POST'])
# @admin_required
# def register() -> tuple:
#     """
#     Register a user.

#     Args
#     ----
#     None

#     Returns
#     -------
#     response (tuple): The response tuple containing the response data and status code.
#     """
#     try:
#         db = current_app.config['database']
#         authenticator = current_app.config['authenticator']
#         username = request.json.get('username')
#         email = request.json.get('email')
#         password = authenticator.encrypt_password(request.json.get('password'))
#         verification_code = authenticator.generate_one_time_code()
#         db.create_user(username, email, password, verification_code)
#         # TODO: SEND VERIFICATION EMAIL
#         return jsonify({"message": "registration successful"}), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/reset-password/', methods=['POST'])
def reset_password() -> tuple:
    """
    Reset a user's password.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        db = current_app.config['database']
        authenticator = current_app.config['authenticator']
        email = request.json.get('email')
        reset_code = request.json.get('reset_code')
        password = authenticator.encrypt_password(request.json.get('password'))
        user = db.get_user_by_email(email)
        authenticator.verify_code(reset_code, user.reset_code)
        db.update_password(user, password)
        return jsonify({"message": "password reset successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/request-password-reset/', methods=['POST'])
def request_password_reset() -> tuple:
    """
    Request a password reset.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        db = current_app.config['database']
        authenticator = current_app.config['authenticator']
        email = request.json.get('email')
        user = db.get_user_by_email(email)
        reset_code = authenticator.generate_one_time_code()
        db.update_reset_code(user, reset_code)
        # TODO: SEND VERIFICATION EMAIL
        return jsonify({"message": "reset code sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/verify/', methods=['POST'])
def verify() -> tuple:
    """
    Verify a user's email using their verification code
    """
    try:
        db = current_app.config['database']
        
        verification_code = request.json.get('verification_code')
        email = request.json.get('email')
        
        if not verification_code or not email:
            return jsonify({"error": "Verification code and email are required"}), 400
            
        # Get user by verification code
        user = db.get_user_by_verification_code(verification_code)
        
        # Verify that the email matches
        if user.email != email:
            return jsonify({"error": "Invalid verification code or email"}), 400
            
        # Verify the user
        db.verify_user(user)
        
        return jsonify({"message": "Email verified successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/delete-user/', methods=['DELETE'])
@admin_required
def delete_user() -> tuple:
    """
    Delete a user.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        db = current_app.config['database']
        user_id = request.json.get('user_id')
        db.delete_user(user_id)
        return jsonify({"message": "user deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/register/', methods=['POST'])
@admin_required
def register() -> tuple:
    """
    Register a new user (admin only).
    Sends verification email to the new user.
    Checks if the email is already in the system.
    """
    try:
        db = current_app.config['database']
        authenticator = current_app.config['authenticator']
        email_manager = current_app.config['email_manager']
        
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')  # Get password from request
        
        if not username or not email or not password:
            return jsonify({"error": "Username, email, and password are required"}), 400

        # Check if the email is already in the system
        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({"error": "Email is already registered"}), 400

        # Generate verification code
        verification_code = authenticator.generate_one_time_code()
        
        # Encrypt the password
        encrypted_password = authenticator.encrypt_password(password)
        
        # Create unverified user with encrypted password
        user = db.create_unverified_user(
            username=username, 
            email=email, 
            password=encrypted_password,
            verification_code=verification_code
        )
        
        # Send verification email
        email_manager.send_verification_email(
            to_email=email,
            username=username,
            verification_code=verification_code
        )
        
        return jsonify({"message": "User registered. Verification email sent."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/get-user-info/', methods=['GET'])
@verified_login_required
def get_user_info() -> tuple:
    """
    Get the user info for the logged in user.
    """
    try:
        db = current_app.config['database']
        user_id = session.get('user_id')
        user = db.get_user_by_id(user_id)
        return jsonify({"user": user.to_dict()}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 401