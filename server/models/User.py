"""
"""

# IMPORTS
from db_config import db


# USER DATA CLASS
class User(db.Model):
    """
    A data class to represent a user in the database.

    Disclaimer
    ----------
    This class was created with the assistance of AI tools (GitHub Copilot). All code created is original and has been reviewed and understood by a human developer.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    reset_code = db.Column(db.String(6), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    scrapes = db.relationship('Scrape', back_populates='user')

    def to_dict(self) -> dict:
        """
        Return the dictionary representation of the user.

        Args
        ----
        None

        Returns
        -------
        dict: The dictionary representation of the user.
        """
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
            "is_verified": self.is_verified,
            "verification_code": self.verification_code,
            "reset_code": self.reset_code,
            "is_admin": self.is_admin,
        }
