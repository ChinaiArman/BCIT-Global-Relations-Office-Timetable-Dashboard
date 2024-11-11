"""
"""

# IMPORTS
from flask import Blueprint, jsonify, request, current_app

from services.decorators import verified_login_required, admin_required


# DEFINE BLUEPRINT
email_bp = Blueprint('email_bp', __name__)


# ROUTES
@email_bp.route('/email/test/', methods=['POST'])
@admin_required  # Only admins should be able to test email functionality
def test_email() -> tuple:
    """
    Test email functionality.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        email_manager = current_app.config['email_manager']
        test_email = request.json.get('email')
        
        if not test_email:
            return jsonify({"error": "Email is required"}), 400
            
        email_manager.send_verification_email(
            to_email=test_email,
            username="Test User",
            verification_code="123456"
        )
        return jsonify({"message": "Test email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@email_bp.route('/email/send-verification/', methods=['POST'])
@admin_required
def send_verification_email() -> tuple:
    """
    Send verification email to a user.

    Args
    ----
    None

    Returns
    -------
    response (tuple): The response tuple containing the response data and status code.
    """
    try:
        email_manager = current_app.config['email_manager']
        authenticator = current_app.config['authenticator']
        
        email = request.json.get('email')
        username = request.json.get('username')
        
        if not email or not username:
            return jsonify({"error": "Email and username are required"}), 400
            
        verification_code = authenticator.generate_one_time_code()
        
        email_manager.send_verification_email(
            to_email=email,
            username=username,
            verification_code=verification_code
        )
        
        return jsonify({
            "message": "Verification email sent successfully",
            "verification_code": verification_code  # In practice, you might not want to return this
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

