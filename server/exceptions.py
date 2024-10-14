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
