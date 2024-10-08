"""
"""

# IMPORTS
from db_config import db
from models.Enrollments import enrollments


# STUDENT DATA CLASS
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String(9), primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    term_code = db.Column(db.Integer, nullable=False)
    preferences = db.Column(db.String(256), default='')

    # Use a string reference for the Course class
    courses = db.relationship('Course', secondary=enrollments, back_populates='students')
