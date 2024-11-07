"""
"""

# IMPORTS
from functools import wraps
from flask import session, jsonify, current_app


# DECORATORS
def login_required(func: callable) -> callable:
    """
    A decorator to require login for a route.

    Args
    ----
    func (callable): The function to decorate.

    Returns
    -------
    wrapper (callable): The decorated function.

    Disclaimer
    ----------
    This function was created with the assistance of AI tools (GitHub Copilot). All code created is original and has been reviewed and understood by a human developer.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        """
        The wrapper function for the decorator.

        Args
        ----
        *args: The arguments for the function.
        **kwargs: The keyword arguments for the function.

        Returns
        -------
        func(*args, **kwargs): The decorated function.

        Disclaimer
        ----------
        This function was created with the assistance of AI tools (GitHub Copilot). All code created is original and has been reviewed and understood by a human developer.
        """
        if "user_id" in session:
            return func(*args, **kwargs)
        else:
            return jsonify({"error": "login required"}), 401
    return wrapper

def admin_required(func: callable) -> callable:
    """
    A decorator to require an admin user for a route.

    Args
    ----
    func (callable): The function to decorate.

    Returns
    -------
    wrapper (callable): The decorated function.

    Disclaimer
    ----------
    This function was created with the assistance of AI tools (GitHub Copilot). All code created is original and has been reviewed and understood by a human developer.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> callable:
        """
        """
        if "user_id" in session:
            db = current_app.config['database']
            user = db.get_user_by_id(session.get('user_id'))
            if user.is_admin:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "admin required"}), 401
        else:
            return jsonify({"error": "login required"}), 401
    return wrapper

