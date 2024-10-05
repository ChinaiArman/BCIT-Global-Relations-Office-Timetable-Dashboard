"""
"""

# IMPORTS


# COURSE DATA CLASS
class Course:
    """
    Represents a course with its details.
    """
    def __init__(self, status: str, block: str, crn: str, course_code: str, course_type: str, day: str, begin_time: int, end_time: int, instructor: str, building_room: str, start_date: str, end_date: str, max_capacity: int, num_enrolled: int, current_students: list):
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
        - num_enrolled (int): The actual number of students enrolled.
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
        self.num_enrolled = num_enrolled
        self.current_students = current_students

    def add_student(self, student):
        """
        Add a student to the course. This will add the Student to the list and increase the actual enrollment by 1.

        Args:
        - student (Student): The student to be added to the course.

        Returns:
        --------
        None

        Notes:
        ------
        1. The student object is added to the `current_students` attribute of the Course instance.
        2. The `actual_enrollment` attribute is incremented by 1.

        Example:
        --------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25, current_students=['123456'])
        >>> course.add_student('654321')
        >>> print(course.current_students)
        ... ['123456', '654321']
        >>> print(course.actual_enrollment)
        ... 26

        Author: ``@KateSullivan``
        """
        self.current_students.append(student)
        self.num_enrolled += 1

    def remove_student(self, student_id: str):
        """
        Remove a student from the course. This will remove the student object from the list and decrease the actual enrollment by 1.

        Args:
        - student_id (str): The student ID of the student to be removed from the course.

        Returns:
        --------
        None

        Notes:
        ------
        1. The student object is removed from the `current_students` attribute of the Course instance.
        2. The `actual_enrollment` attribute is decremented by 1.

        Example:
        --------
        >>> course = Course(status='Active', block='A', crn='12345', course_code='CS101', course_type='Lecture', day='Monday', begin_time=9, end_time=10, instructor='John Doe', building_room='Building A, Room 101', start_date='2022-01-01', end_date='2022-05-01', max_capacity=30, actual_enrollment=25, current_students=['123456'])
        >>> course.remove_student('123456')
        >>> print(course.current_students)
        ... []
        >>> print(course.actual_enrollment)
        ... 24

        Author: ``@KateSullivan``
        """
        # find the student in the list by id
        self.current_students = [student for student in self.current_students if student.id != student_id]
        self.num_enrolled -= 1
    