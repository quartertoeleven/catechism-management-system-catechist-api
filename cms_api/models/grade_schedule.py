from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date, Boolean

from .base import db
from ..helpers.enums import SemesterEnum


class GradeSchedule(db.Model):
    __tablename__ = "grade_schedules"

    id = Column(Integer, primary_key=True)
    semester = Column(Enum(SemesterEnum), nullable=False)
    date = Column(Date, nullable=False)
    mass_content = Column(String(100), nullable=False)
    is_mass_attendance_check = Column(Boolean, nullable=False, default=True, server_default="true")
    lesson_content = Column(String(100), nullable=False)
    is_lesson_attendance_check = Column(Boolean, nullable=False, default=True, server_default="true")
    general_schedule_id = Column(
        ForeignKey("general_schedules.id", ondelete="set null", onupdate="set null")
    )
    grade_id = Column(
        ForeignKey("grades.id", ondelete="cascade", onupdate="cascade"), nullable=False
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
