"""
"""

# IMPORTS
import logging
from logging.handlers import RotatingFileHandler
import os


# CONFIG LOGGING
def configure_logging(app) -> None:
    """
    Configure the logging for the application to write to two log files: app.log and error.log

    Args:
    -----
    app (Flask): The Flask application instance.

    Returns:
    --------
    None

    Notes:
    ------
    1. The app.log file contains INFO logs.
    2. The error.log file contains ERROR logs.
    3. The log files are stored in the `server/logs/` directory.

    Example:
    --------
    >>> app = Flask(__name__)
    >>> configure_logging(app)
    ... # Log files created in `server/logs/` directory

    Author: ``@ChinaiArman``
    """
    init_log_files()
    app.logger.setLevel(logging.INFO)
    file_handler = RotatingFileHandler('server/logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)

    error_handler = RotatingFileHandler('server/logs/error.log', maxBytes=10240, backupCount=10)
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    app.logger.addHandler(error_handler)
    return


def init_log_files() -> None:
    """
    Initialize the log files for the application.

    Args:
    -----
    None

    Returns:
    --------
    None

    Notes:
    ------
    1. The log files are stored in the `server/logs/` directory.
    2. The log files are created if they do not exist.

    Example:
    --------
    >>> init_log_files()
    ... # Log files created in `server/logs/` directory

    Author: ``@ChinaiArman``
    """
    if not os.path.exists('server/logs'):
        os.makedirs('server/logs')

    if not os.path.exists('server/logs/app.log'):
        with open('server/logs/app.log', 'w') as f:
            f.write('')
    
    if not os.path.exists('server/logs/error.log'):
        with open('server/logs/error.log', 'w') as f:
            f.write('')
    return
