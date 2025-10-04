from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date, Boolean

from .base import db
from ..helpers.enums import SemesterEnum
from . import Grade


class GradeSchedule(db.Model):
    __tablename__ = "grade_schedules"

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
    general_schedule_id = Column(
        ForeignKey("general_schedules.id", ondelete="set null", onupdate="set null")
    )
    grade_id = Column(
        ForeignKey("grades.id", ondelete="cascade", onupdate="cascade"), nullable=False
    )

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_schedules_for_grade(cls, grade: Grade):
        return cls.query.filter_by(grade_id=grade.id).order_by(cls.date.desc()).all()

    def to_dict(self):
        return dict(
            id=self.id,
            semester=self.semester.value,
            date=self.date,
            mass_content=self.mass_content,
            is_mass_attendance_check=self.is_mass_attendance_check,
            lesson_content=self.lesson_content,
            is_lesson_attendance_check=self.is_lesson_attendance_check,
            general_schedule_id=self.general_schedule_id,
            grade_id=self.grade_id,
        )
