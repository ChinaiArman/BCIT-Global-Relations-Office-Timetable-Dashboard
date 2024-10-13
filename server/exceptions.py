"""
"""


class InvalidUploadFile(Exception):
    """
    Raised when an invalid file is uploaded.
    """

    pass


class DatabaseError(Exception):
    """
    Raised when an error occurs in the database
    """

    def __init__(self, message, status_code=500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

    def to_dict(self):
        return {"status": self.status_code, "error": self.message}


class DataNotFound(DatabaseError):
    """
    Raised when an invalid request is made
    """

    def __init__(self, message, status_code=404):
        super().__init__(f"{message} not found in Database", status_code)


class DataAlreadyExists(DatabaseError):
    """
    Raised when an invalid request is made
    """

    def __init__(self, message, status_code=400):
        super().__init__(f"{message} already exists in Database", status_code)
