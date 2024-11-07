"""
"""

# IMPORTS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


# ENVIRONMENT VARIABLES
load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


# INIT DATABASE
db = SQLAlchemy()


# CONFIGURE DATABASE
def configure_db(app) -> None:
    """
    Configure the MYSQL database connection.

    Args:
    -----
    app (Flask): The Flask application instance.

    Returns:
    --------
    None

    Notes:
    ------
    1. The database connection is configured using the environment variables.
    2. The database connection is initialized.

    Example:
    --------
    >>> configure_db(app)
    ... # Database connection configured

    Author: ``@ChinaiArman``
    """
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return
