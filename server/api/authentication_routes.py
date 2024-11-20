"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app, session
import random

from services.decorators import verified_login_required, admin_required, unverified_login_required
from exceptions import InvalidEmailAddress


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
@unverified_login_required
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
        session.permanent = True
        session["user_id"] = user.id
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
        email_manager = current_app.config['email_manager']
        email = request.json.get('email')
        user = db.get_user_by_email(email)
        reset_code = authenticator.generate_one_time_code()
        db.update_reset_code(user, reset_code)
        email_manager.forgot_password_email(email, reset_code)
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
        authenticator = current_app.config['authenticator']
        
        verification_code = request.json.get('verification_code')
        new_password = request.json.get('new_password')
        email = request.json.get('email')
        
        if not verification_code or not email or not new_password:
            return jsonify({"error": "Verification code, email, new password are required"}), 400
            
        # Get user by email
        user = db.get_user_by_email(email)
        
        # Verify that the email matches
        if user.verification_code != verification_code:
            return jsonify({"error": "Invalid verification code or email"}), 400
            
        # Encrypt the new password
        new_password = authenticator.encrypt_password(new_password)

        # Verify the user
        db.verify_user_with_password(user, new_password)
        
        # Log the user in
        session.permanent = True
        session["user_id"] = user.id
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
        # generate a password starting with PW, followed by 6 random digits, and ! at the end
        password = "PW" + str(random.randint(100000, 999999)) + "!"
        
        if not username or not email:
            return jsonify({"error": "Username, email, and password are required"}), 400

        # Check if the email is already in the system
        try:
            existing_user = db.get_user_by_email(email)
            return jsonify({"error": "Email is already registered"}), 400
        except InvalidEmailAddress as e:
            existing_user = False
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
    

@authentication_bp.route('/authenticate/is-admin/', methods=['GET'])
@admin_required
def is_admin() -> tuple:
    """
    Check if the user is an admin.
    """
    try:
        return jsonify({"message": "User is an admin"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@authentication_bp.route('/authenticate/is-verified/', methods=['GET'])
@verified_login_required
def is_verified() -> tuple:
    """
    Check if the user is verified.
    """
    try:
        return jsonify({"message": "User is verified"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@authentication_bp.route('/authenticate/is-unverified/', methods=['GET'])
@unverified_login_required
def is_unverified() -> tuple:
    """
    Check if the user is unverified.
    """
    try:
        return jsonify({"message": "User is unverified"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    

@authentication_bp.route('/authenticate/get-users/', methods=['GET'])
@admin_required
def get_all_users_info() -> tuple:
    """
    Get the user info for all users.
    """
    try:
        db = current_app.config['database']
        response = db.get_all_users_info()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
    
@authentication_bp.route('/authenticate/change-role/', methods=['PATCH'])
@admin_required
def change_user_role() -> tuple:
    """
    Change the role of a specific user.
    """
    try:
        db = current_app.config['database']
        user_id = request.json.get('user_id')
        
        if not user_id:
            return jsonify({"error": "user_id required"}), 400

        db.change_user_admin_status(user_id)
        
        return jsonify({"message": f"Role for user {user_id} successfully updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@authentication_bp.route('/authenticate/change-password/', methods=['PUT'])
@verified_login_required
def change_password() -> tuple:
    """
    Change the password of the logged in user.
    """
    try:
        db = current_app.config['database']
        authenticator = current_app.config['authenticator']
        user_id = session.get('user_id')
        user = db.get_user_by_id(user_id)
        old_password = request.json.get('oldPassword')
        new_password = request.json.get('password')
        
        if not old_password or not new_password:
            return jsonify({"error": "Old password and new password are required"}), 400
        
        authenticator.verify_password(old_password, user.password)
        encrypted_new_password = authenticator.encrypt_password(new_password)
        db.update_password(user, encrypted_new_password)
        
        return jsonify({"message": "Password successfully updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
    
@authentication_bp.route('/authenticate/update-user-info/', methods=['PUT'])
@verified_login_required
def update_user_info() -> tuple:
    """
    Update the user info for the logged in user.
    """
    try:
        db = current_app.config['database']
        user_id = session.get('user_id')
        username = request.json.get('username')
        email = request.json.get('email')
        
        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400
        
        db.update_user_info(user_id, username, email)
        
        return jsonify({"message": "User info successfully updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401
        