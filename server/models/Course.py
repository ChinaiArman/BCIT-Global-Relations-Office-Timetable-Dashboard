"""
"""

# IMPORTS
from sql_db import db
from models.Enrollments import enrollments


# COURSE DATA CLASS
class Course(db.Model):
    """
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(10), nullable=False)
    block = db.Column(db.String(10), nullable=False)
    crn = db.Column(db.Integer, nullable=False)
    course_grouping = db.Column(db.String(20), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    course_type = db.Column(db.String(10), nullable=False)
    day = db.Column(db.String(20), nullable=False)
    begin_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building_room = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    num_enrolled = db.Column(db.Integer, default=0)
    is_full_time = db.Column(db.String(20), nullable=False)
    term_code = db.Column(db.String(10), nullable=False)
    instructor = db.Column(db.String(256), nullable=False)

    students = db.relationship('Student', secondary=enrollments, back_populates='courses')

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
        if self.num_enrolled < self.max_capacity:
            self.current_students.append(student)
            self.num_enrolled += 1

    def remove_student(self, student: str):
        """
        Remove a student from the course. This will remove the student object from the list and decrease the actual enrollment by 1.

        Args:
        - student (str): The student object to be removed from the course.

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
        >>> student = Student(id='123456', first_name='Jane', last_name='Doe', student_email='jane_doe@bcit.ca', selection
        >>> course.remove_student(student)
        >>> print(course.current_students)
        ... []
        >>> print(course.actual_enrollment)
        ... 24

        Author: ``@KateSullivan``
        """
        if student in self.current_students:
            self.current_students.remove(student)
            self.num_enrolled -= 1
    