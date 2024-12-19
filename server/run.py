"""
"""

# IMPORTS
from dotenv import load_dotenv
import os

from app import create_app


# ENVIRONMENT VARIABLES
load_dotenv()
PORT = os.getenv('PORT', 8000)


# CREATE APP
app, db = create_app()


# MAIN
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(port=PORT, debug=True)
