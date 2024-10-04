"""
"""

# IMPORTS


# SCHEDULE DATA CLASS
class Schedule:
    """
    """
    def __init__(self, courses: list, student_id: str):
        """
        """
        self.courses = courses
        self.student_id = student_id

    def get_courses(self):
        """
        """
        return self.courses

    def get_student_id(self):
        """
        """
        return self.student_id