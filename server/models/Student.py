"""
"""

# IMPORTS
from db_config import db
from models.Enrollments import enrollments


# STUDENT DATA CLASS
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.String(9), primary_key=True, autoincrement=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    term_code = db.Column(db.Integer, nullable=False)

    preferences = db.relationship("Preferences", back_populates="student")
    courses = db.relationship(
        "Course", secondary=enrollments, back_populates="students"
    )

    def __repr__(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "term_code": self.term_code,
            "preferences": [course.preference for course in self.preferences],
            "courses": [course.course_code for course in self.courses],
        }
