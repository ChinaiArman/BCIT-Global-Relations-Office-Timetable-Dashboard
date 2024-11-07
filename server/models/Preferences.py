"""
"""

# IMPORTS
from db_config import db

class Preferences(db.Model):
    __tablename__ = "preferences"

    student_id = db.Column(db.String(9), db.ForeignKey("students.id"), primary_key=True)
    priority = db.Column(db.Integer, primary_key=True)
    preference = db.Column(db.String(8), nullable=False) 
    student = db.relationship("Student", back_populates="preferences")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "priority": self.priority,
            "course_code": self.preference,
        }