"""
"""

# IMPORTS


# STUDENT DATA CLASS
class Student:
    """ """

    def __init__(
        self, id: str, firstName: str, lastName: str, selection: list=[], courses: list=[]
    ):
        """
        Intialize the Student instance.

        Args:
        -----
        - id (str): The student ID.
        - firstName (str): The first name of the student.
        - lastName (str): The last name of the student.
        - selection (list): A list of Course instances selected by the student.
        - courses (list): A list of Course instances assigned to the student.

        Author: ``@CharlieZhang``
        """
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.selection = selection
        self.courses = courses
