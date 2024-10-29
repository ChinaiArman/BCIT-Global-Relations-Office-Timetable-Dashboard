"""
"""

# IMPORTS
from db_config import db


# PREFERENCES TABLE
preferences = db.Table(
    "preferences",
    db.Column("student_id", db.String(9), db.ForeignKey("students.id"), primary_key=True),
    db.Column("priority", db.Integer, primary_key=True),
    db.Column("course_code", db.String(8), nullable=False),
)
