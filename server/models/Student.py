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
    email = db.Column(db.String(100), nullable=False, unique=True)
    term_code = db.Column(db.Integer, nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    preferences = db.relationship("Preferences", back_populates="student")
    courses = db.relationship(
        "Course", secondary=enrollments, back_populates="students"
    )

    def to_dict(self):
        student = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "term_code": self.term_code,
            "email": self.email,
            "is_completed": self.is_completed,
            "preferences": [course.preference for course in self.preferences],
            "courses": []
        }
        for course in self.courses:
            course.start_date = course.start_date.strftime("%Y-%m-%d")
            course.end_date = course.end_date.strftime("%Y-%m-%d")
            course.begin_time = course.begin_time.strftime("%H:%M")
            course.end_time = course.end_time.strftime("%H:%M")
            student["courses"].append(course.to_dict())
        return student
