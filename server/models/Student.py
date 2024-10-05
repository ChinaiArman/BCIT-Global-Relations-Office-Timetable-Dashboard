"""
"""

# IMPORTS


# STUDENT DATA CLASS
class Student:
    """ """

    def __init__(
        self, id: str, firstName: str, lastName: str, selection: list, courses: list
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

        author: ``@CharlieZhang``
        """
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.selection = selection
        self.courses = courses

    def get_id(self) -> str:
        """
        Get the student ID.

        Args:
        -----
        None

        Returns:
        --------
        ``str``
            The student ID.

        Notes:
        ------
        1. The student ID is stored in the `id` attribute of the Student instance.

        Example:
        --------
        >>> student = Student(id='123456', firstName='John', lastName='Doe', selection=[], courses=[])
        >>> student.get_id()
        ... '123456'

        Author: ``@CharlieZhang``
        """
        return self.id

    def get_first_name(self) -> str:
        """
        Get the first name of the student.

        Args:
        -----
        None

        Returns:
        --------
        ``str``
            The first name of the student.

        Notes:
        ------
        1. The first name is stored in the `firstName` attribute of the Student instance.

        Example:
        --------
        >>> student = Student(id='123456', firstName='John', lastName='Doe', selection=[], courses=[])
        >>> student.get_first_name()
        ... 'John'

        Author: ``@CharlieZhang``
        """
        return self.firstName

    def get_last_name(self) -> str:
        """
        Get the last name of the student.

        Args:
        -----
        None

        Returns:
        --------
        ``str``
            The last name of the student.

        Notes:
        ------
        1. The last name is stored in the `lastName` attribute of the Student instance.

        Example:
        --------
        >>> student = Student(id='123456', firstName='John', lastName='Doe', selection=[], courses=[])
        >>> student.get_last_name()
        ... 'Doe'

        Author: ``@CharlieZhang``
        """
        return self.lastName

    def get_selection(self) -> list:
        """
        Get the selection of the student.

        Args:
        -----
        None

        Returns:
        --------
        ``list``
            A list of Course instances selected by the student.

        Notes:
        ------
        1. The list of selections is stored in the `selection` attribute of the Student instance.

        Example:
        --------
        >>> student = Student(id='123456', firstName='John', lastName='Doe', selection=[course1, course2, course3], courses=[])
        >>> student.get_selection()
        ... [course1, course2, course3]

        Author: ``@CharlieZhang``
        """
        return self.selection

    def get_courses(self) -> list:
        """
        Get the courses of the student.

        Args:
        -----
        None

        Returns:
        --------
        ``list``
            A list of Course instances assigned to the student.

        Notes:
        ------
        1. The list of courses is stored in the `courses` attribute of the Student instance.

        Example:
        --------
        >>> student = Student(id='123456', firstName='John', lastName='Doe', selection=[], courses=[course1, course2, course3])
        >>> student.get_courses()
        ... [course1, course2, course3]

        Author: ``@CharlieZhang``
        """
        return self.courses
