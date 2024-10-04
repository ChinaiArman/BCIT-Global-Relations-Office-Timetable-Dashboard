"""
"""

# IMPORTS
from services.Authenticator import Authenticator
from services.Database import Database
from services.EmailManager import EmailManager
from services.CourseManager import CourseManager
from services.StudentManager import StudentManager


# CONTROLLER CLASS
class Controller:
    """
    """
    def __init__(self):
        """
        """
        self.authenticator = Authenticator()
        self.database = Database()
        self.email_manager = EmailManager()
        self.course_manager = CourseManager()
        self.student_manager = StudentManager()

    