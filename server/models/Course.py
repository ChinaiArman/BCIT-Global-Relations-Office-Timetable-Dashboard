"""
"""

# IMPORTS


# COURSE DATA CLASS
class Course:
    """
    Represents a course with its details.
    """
    def __init__(self, status: str, block: str, crn: str, course_code: str, course_type: str, day: str, begin_time: int, end_time: int, instructor: str, building_room: str, start_date: str, end_date: str, max_capacity: int, actual_enrollment: int, current_students: list):
        """
        Initializes a Course instance with its details.

        Args:
        - status (str): The status of the course.
        - block (str): The block of the course.
        - crn (str): The Course Registration Number.
        - course_code (str): The code of the course.
        - course_type (str): The type of the course.
        - day (str): The day of the week the course is held.
        - begin_time (int): The start time of the course.
        - end_time (int): The end time of the course.
        - instructor (str): The instructor teaching the course.
        - building_room (str): The building and room where the course is held.
        - start_date (str): The start date of the course.
        - end_date (str): The end date of the course.
        - max_capacity (int): The maximum capacity of the course.
        - actual_enrollment (int): The actual number of students enrolled.
        - current_students (list): A list of students currently enrolled in the course.
        """
        self.status = status
        self.block = block
        self.crn = crn
        self.course_code = course_code
        self.course_type = course_type
        self.day = day
        self.begin_time = begin_time
        self.end_time = end_time
        self.instructor = instructor
        self.building_room = building_room
        self.start_date = start_date
        self.end_date = end_date
        self.max_capacity = max_capacity
        self.actual_enrollment = actual_enrollment
        self.current_students = current_students

    def get_status(self) -> str:
        """
        Get the status of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The status of the course.

        Notes:
        -----
        1. The status is stored in the `status` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_status()
        ... 'Active'

        Author: ``@KateSullivan``
        """
        return self.status

    def get_block(self) -> str:
        """
        Get the block of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The block of the course.

        Notes:
        -----
        1. The block is stored in the `block` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_block()
        ... 'A'

        Author: ``@KateSullivan``
        """
        return self.block

    def get_crn(self) -> str:
        """
        Get the Course Registration Number (CRN) of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The CRN of the course.

        Notes:
        -----
        1. The CRN is stored in the `crn` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_crn()
        ... '12345'

        Author: ``@KateSullivan``
        """
        return self.crn

    def get_course_code(self) -> str:
        """
        Get the course code of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The course code of the course.

        Notes:
        -----
        1. The course code is stored in the `course_code` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_course_code()
        ... 'CS101'

        Author: ``@KateSullivan``
        """
        return self.course_code

    def get_course_type(self) -> str:
        """
        Get the type of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The type of the course.

        Notes:
        -----
        1. The course type is stored in the `course_type` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_course_type()
        ... 'Lecture'

        Author: ``@KateSullivan``
        """
        return self.course_type

    def get_day(self) -> str:
        """
        Get the day of the week the course is held.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The day of the week the course is held.

        Notes:
        -----
        1. The day is stored in the `day` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_day()
        ... 'Monday'

        Author: ``@KateSullivan``
        """
        return self.day

    def get_begin_time(self) -> int:
        """
        Get the start time of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``int``
            The start time of the course.

        Notes:
        -----
        1. The start time is stored in the `begin_time` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_begin_time()
        ... 9

        Author: ``@KateSullivan``
        """
        return self.begin_time

    def get_end_time(self) -> int:
        """
        Get the end time of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``int``
            The end time of the course.

        Notes:
        -----
        1. The end time is stored in the `end_time` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_end_time()
        ... 10

        Author: ``@KateSullivan``
        """
        return self.end_time

    def get_instructor(self) -> str:
        """
        Get the instructor teaching the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The instructor teaching the course.

        Notes:
        -----
        1. The instructor is stored in the `instructor` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_instructor()
        ... 'John Doe'

        Author: ``@KateSullivan``
        """
        return self.instructor

    def get_building_room(self) -> str:
        """
        Get the building and room where the course is held.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The building and room where the course is held.

        Notes:
        -----
        1. The building and room are stored in the `building_room` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_building_room()
        ... 'Building A, Room 101'

        Author: ``@KateSullivan``
        """
        return self.building_room

    def get_start_date(self) -> str:
        """
        Get the start date of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The start date of the course.

        Notes:
        -----
        1. The start date is stored in the `start_date` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_start_date()
        ... '2022-01-01'

        Author: ``@KateSullivan``
        """
        return self.start_date

    def get_end_date(self) -> str:
        """
        Get the end date of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``str``
            The end date of the course.

        Notes:
        -----
        1. The end date is stored in the `end_date` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_end_date()
        ... '2022-05-01'

        Author: ``@KateSullivan``
        """
        return self.end_date

    def get_max_capacity(self) -> int:
        """
        Get the maximum capacity of the course.

        Args:
        -----
        None

        Returns:
        -------
        ``int``
            The maximum capacity of the course.

        Notes:
        -----
        1. The maximum capacity is stored in the `max_capacity` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_max_capacity()
        ... 30

        Author: ``@KateSullivan``
        """
        return self.max_capacity

    def get_actual_enrollment(self) -> int:
        """
        Get the actual number of students enrolled in the course.

        Args:
        -----
        None

        Returns:
        -------
        ``int``
            The actual number of students enrolled in the course.

        Notes:
        -----
        1. The actual enrollment is stored in the `actual_enrollment` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.get_actual_enrollment()
        ... 25

        Author: ``@KateSullivan``
        """
        return self.actual_enrollment

    def get_current_students(self) -> list:
        """
        Get the list of students currently enrolled in the course.

        Args:
        -----
        None

        Returns:
        -------
        ``list``
            A list of student IDs currently enrolled in the course.

        Notes:
        -----
        1. The list of students is stored in the `current_students` attribute of the Course instance.

        Example:
        -------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25, current_students=['123456'])
        >>> course.get_current_students()
        ... ['123456']

        Author: ``@KateSullivan``
        """
        return self.current_students

    def set_actual_enrollment(self, actual_enrollment: int):
        """
        Set the actual number of students enrolled in the course.

        Args:
        - actual_enrollment (int): The actual number of students enrolled in the course.

        Returns:
        --------
        None

        Notes:
        ------
        1. The actual enrollment is stored in the `actual_enrollment` attribute of the Course instance.

        Example:
        --------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25)
        >>> course.set_actual_enrollment(26)
        >>> course.get_actual_enrollment()
        ... 26

        Author: ``@KateSullivan``
        """

    def add_student(self, student_id: str):
        """
        Add a student to the course. This will add the student ID to the list and increase the actual enrollment by 1.

        Args:
        - student_id (str): The student ID of the student to be added to the course.

        Returns:
        --------
        None

        Notes:
        ------
        1. The student ID is added to the `current_students` attribute of the Course instance.
        2. The `actual_enrollment` attribute is incremented by 1.

        Example:
        --------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25, current_students=['123456'])
        >>> course.add_student('654321')
        >>> course.get_current_students()
        ... ['123456', '654321']
        >>> course.get_actual_enrollment()
        ... 26

        Author: ``@KateSullivan``
        """

        current_students = self.get_current_students()
        current_students.append(student_id)
        number_of_students = self.get_actual_enrollment()
        number_of_students += 1
        self.set_actual_enrollment(number_of_students)

    def remove_student(self, student_id: str):
        """
        Remove a student from the course. This will remove the student ID from the list and decrease the actual enrollment by 1.

        Args:
        - student_id (str): The student ID of the student to be removed from the course.

        Returns:
        --------
        None

        Notes:
        ------
        1. The student ID is removed from the `current_students` attribute of the Course instance.
        2. The `actual_enrollment` attribute is decremented by 1.

        Example:
        --------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25, current_students=['123456'])
        >>> course.remove_student('123456')
        >>> course.get_current_students()
        ... []
        >>> course.get_actual_enrollment()
        ... 24

        Author: ``@KateSullivan``
        """

        current_students = self.get_current_students()
        current_students.remove(student_id)
        number_of_students = self.get_actual_enrollment()
        number_of_students -= 1
        self.set_actual_enrollment(number_of_students)



        



    