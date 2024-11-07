"""
"""

# IMPORTS
from flask_session import Session
from datetime import timedelta


# CONFIGURE SESSIONS
def configure_sessions(app, db) -> None:
    """
    Configure the Flask application sessions.

    Args
    ----
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.

    Returns
    -------
    None

    Disclaimer
    ----------
    This method was created with the assistance of AI tools (GitHub Copilot). All code created is original and has been reviewed and understood by a human developer.
    """
    app.config['SECRET_KEY'] = 'imsosleepybruh'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['SESSION_SQLALCHEMY_TABLE'] = 'sessions'
    app.config['SESSION_USE_SIGNER'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(weeks=2)
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    Session(app)
    return
