from sqlalchemy import Column, String, Enum, Integer, ForeignKey, Date, Boolean, PrimaryKeyConstraint, DateTime
from sqlalchemy.dialects.postgresql import UUID

from .base import db
from ..helpers.enums import AttendanceStatusEnum


class StudentAttendance(db.Model):
    __tablename__ = "student_attendances"
    __table_args__ = (
        PrimaryKeyConstraint("student_id", "grade_schedule_id"),
    )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
        nullable=False
    )
    grade_schedule_id = Column(
        Integer,
        ForeignKey("grade_schedules.id", ondelete="cascade", onupdate="cascade"),
        nullable=False
    )
    mass_status = Column(Enum(AttendanceStatusEnum), nullable=False, default=AttendanceStatusEnum.ABSENT, server_default=AttendanceStatusEnum.ABSENT.name)
    is_mass_absence_notified = Column(Boolean, default=False, server_default="false")
    lesson_status = Column(Enum(AttendanceStatusEnum), nullable=False, default=AttendanceStatusEnum.ABSENT, server_default=AttendanceStatusEnum.ABSENT.name)
    is_lesson_absence_notified = Column(Boolean, default=False, server_default="false")
    mass_absence_reason = Column(String(100))
    lesson_absence_reason = Column(String(100))
    catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"),
    )
    check_time = Column(DateTime)
