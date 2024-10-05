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

    def get_courses(self) -> list:
        """
        Get the courses of the schedule.

        Args:
        -----
        None

        Returns:
        --------
        ``list``: A list of Course instances assigned to the student's schedule.

        Notes:
        ------
        1. The list of courses is stored in the `courses` attribute of the Schedule instance.

        Example:
        --------
        >>> schedule = Schedule(courses=[course1, course2, course3], student_id='123456')
        >>> schedule.get_courses()
        ... [course1, course2, course3]

        Author: @ChinaiArman
        """
        return self.courses

    def get_student_id(self) -> str:
        """
        Get the student ID of the schedule.

        Args:
        -----
        None

        Returns:
        --------
        ``str``: The student ID assigned to the schedule.

        Notes:
        ------
        1. The student ID is stored in the `student_id` attribute of the Schedule instance.

        Example:
        --------
        >>> schedule = Schedule(courses=[course1, course2, course3], student_id='123456')
        >>> schedule.get_student_id()
        ... '123456'

        Author: @ChinaiArman
        """
        return self.student_id
