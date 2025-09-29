from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date, Boolean

from .base import db
from ..helpers.enums import SemesterEnum


class GeneralSchedule(db.Model):
    __tablename__ = "general_schedules"

    id = Column(Integer, primary_key=True)
    semester = Column(Enum(SemesterEnum), nullable=False)
    date = Column(Date, nullable=False)
    mass_content = Column(String(100), nullable=False)
    is_mass_attendance_check = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    lesson_content = Column(String(100), nullable=False)
    is_lesson_attendance_check = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    study_year_id = Column(
        ForeignKey("study_years.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
