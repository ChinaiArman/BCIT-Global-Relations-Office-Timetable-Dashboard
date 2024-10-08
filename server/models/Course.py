"""
"""

# IMPORTS
from db_config import db
from models.Enrollments import enrollments


# COURSE DATA CLASS
class Course(db.Model):
    """
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    status = db.Column(db.String(8), nullable=False)
    block = db.Column(db.String(8), nullable=False)
    crn = db.Column(db.Integer, nullable=False)
    course_grouping = db.Column(db.String(16), nullable=False)
    course_code = db.Column(db.String(8), nullable=False)
    course_type = db.Column(db.String(3), nullable=False)
    day = db.Column(db.String(3), nullable=False)
    begin_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    building_room = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    num_enrolled = db.Column(db.Integer, default=0)
    is_full_time = db.Column(db.Boolean, nullable=False)
    term_code = db.Column(db.String(6), nullable=False)
    instructor = db.Column(db.String(512), nullable=False)

    students = db.relationship('Student', secondary=enrollments, back_populates='courses')
