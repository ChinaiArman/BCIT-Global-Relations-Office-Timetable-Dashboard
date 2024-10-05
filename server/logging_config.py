"""
"""

# IMPORTS
import logging
from logging.handlers import RotatingFileHandler


# CONFIG LOGGING
def configure_logging(app) -> None:
    """
    """
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