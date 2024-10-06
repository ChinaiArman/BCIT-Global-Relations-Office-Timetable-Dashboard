"""
"""

# IMPORTS
from sql_db import db


# ENROLLMENTS TABLE
enrollments = db.Table('enrollments',
    db.Column('student_id', db.String(10), db.ForeignKey('students.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.id'), primary_key=True)
)