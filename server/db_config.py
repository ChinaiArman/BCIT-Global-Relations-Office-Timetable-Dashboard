"""
"""

# IMPORTS
from flask_sqlalchemy import SQLAlchemy
import ssl
import os
from dotenv import load_dotenv


# ENVIRONMENT VARIABLES
load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_SSL_CERT = os.getenv('DB_SSL_CERT')


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
    if not DB_SSL_CERT:
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
    else:
        ssl_context = ssl.create_default_context()

        # Load the certificate into the SSLContext
        ssl_context.load_verify_locations(cadata=DB_SSL_CERT)

        # Disable certificate verification to bypass the self-signed cert issue
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        # Set the database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = (
            f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )

        # Pass the SSL context directly in the connect_args
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'connect_args': {
                'ssl': ssl_context  # Pass the SSLContext with the loaded certificate
            }
        }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return