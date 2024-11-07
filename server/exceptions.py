"""
"""

class InvalidUploadFile(Exception):
    """
    Raised when an invalid file is uploaded.
    """
    def __init__(self, message="Invalid file uploaded."):
        self.message = message
        super().__init__(self.message)


class InvalidFileType(Exception):
    """
    Raised when an invalid file type is uploaded.
    """
    def __init__(self, message="Invalid file type uploaded."):
        self.message = message
        super().__init__(self.message)


class DatabaseError(Exception):
    """
    Raised when an error occurs in the database
    """
    def __init__(self, message="Database Error"):
        self.message = message
        super().__init__(self.message)


class DataNotFound(DatabaseError):
    """
    Raised when an invalid request is made
    """
    def __init__(self, message="Data not found."):
        self.message = message
        super().__init__(self.message)


class DataAlreadyExists(DatabaseError):
    """
    Raised when an invalid request is made
    """
    def __init__(self, message="Data already exists."):
        self.message = message
        super().__init__(self.message)

class IncorrectPassword(Exception):
    """
    Raised when an incorrect password is entered
    """
    def __init__(self, message="Incorrect password."):
        self.message = message
        super().__init__(self.message)

class InvalidOneTimeCode(Exception):
    """
    Raised when an invalid one-time code is entered
    """
    def __init__(self, message="Invalid one-time code."):
        self.message = message
        super().__init__(self.message)

class InvalidEmailAddress(Exception):
    """
    An error occurred if the email address is invalid.
    """
    def __init__(self, message="Invalid email address"):
        """
        Constructor for InvalidEmailAddress class.

        Args
        ----
        message (str): Exception message.
        """
        self.message = message
        super().__init__(self.message)

class EmailAddressAlreadyInUse(Exception):
    """
    An error occurred if the email address is already in use.
    """
    def __init__(self, message="Email address already in use"):
        """
        Constructor for EmailAddressAlreadyInUse class.

        Args
        ----
        message (str): Exception message.
        """
        self.message = message
        super().__init__(self.message)

class UserNotFound(Exception):
    """
    An error occurred if the user is not found.
    """
    def __init__(self, message="Invalid user ID"):
        """
        Constructor for UserNotFound class.

        Args
        ----
        message (str): Exception message.
        """
        self.message = message
        super().__init__(self.message)