"""
"""

# IMPORTS
import bcrypt
import secrets

from exceptions import IncorrectPassword, InvalidOneTimeCode


# AUTHENTICATOR CLASS
class Authenticator:
    """
    A class used to authenticate users, sessions, requests, and API keys.
    """
    def __init__(self):
        """
        Initialize the Authenticator class.

        Args
        ----
        None
        """
        pass
    
    def encrypt_password(self, password: str) -> str:
        """
        Encrypt a password.

        Args
        ----
        password (str): The password to encrypt.

        Returns
        -------
        str: The encrypted password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verify a password.

        Args
        ----
        password (str): The password to verify.
        hashed_password (str): The hashed password to compare.

        Returns
        -------
        bool: True if the password is correct, otherwise False.

        Raises
        ------
        IncorrectPassword: If the password is incorrect.
        """
        if not bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
            raise IncorrectPassword()
        return True
    
    def generate_one_time_code(self) -> str:
        """
        Generate a new 6 digit code.

        Args
        ----
        None

        Returns
        -------
        str: The new 6 digit code.
        """
        return secrets.token_hex(3)
    
    def verify_code(self, code: str, user_code: str) -> bool:
        """
        Verify a one-time code.

        Args
        ----
        code (str): The one-time code to verify.
        user_code (str): The user's one-time code.

        Returns
        -------
        bool: True if the one-time code is correct, otherwise False.

        Raises
        ------
        InvalidOneTimeCode: If the one-time code is incorrect.
        """
        if code != user_code or not user_code:
            raise InvalidOneTimeCode()
        return True
