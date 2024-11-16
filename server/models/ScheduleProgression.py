"""
"""

# IMPORTS
from db_config import db


# SCHEDULE PROGRESSION DATA CLASS
class ScheduleProgression(db.Model):
    """
    """
    __tablename__ = 'schedule_progression'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    num_schedules_completed = db.Column(db.Integer, nullable=False)
    num_approvals_from_program_heads = db.Column(db.Integer, nullable=False)