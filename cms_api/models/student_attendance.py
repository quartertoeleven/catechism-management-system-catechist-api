from sqlalchemy import (
    Column,
    String,
    Enum,
    Integer,
    ForeignKey,
    Date,
    Boolean,
    PrimaryKeyConstraint,
    DateTime,
)
from sqlalchemy.dialects.postgresql import UUID

from .base import db
from . import Student, GradeSchedule
from ..helpers.enums import AttendanceStatusEnum, AttendanceTypeEnum


class StudentAttendance(db.Model):
    __tablename__ = "student_attendances"
    __table_args__ = (PrimaryKeyConstraint("student_id", "grade_schedule_id", "type"),)

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
    grade_schedule_id = Column(
        Integer,
        ForeignKey("grade_schedules.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
    type = Column(Enum(AttendanceTypeEnum), nullable=False)
    status = Column(
        Enum(AttendanceStatusEnum),
        nullable=False,
        default=AttendanceStatusEnum.ABSENT,
        server_default=AttendanceStatusEnum.ABSENT.name,
    )
    is_notified_absence = Column(Boolean, default=False, server_default="false")
    note = Column(String(100))
    catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"),
    )
    check_time = Column(DateTime)

    @classmethod
    def find_by_grade_schedule_id_and_student_id(cls, grade_schedule_id, student_id):
        return cls.query.filter_by(
            student_id=student_id, grade_schedule_id=grade_schedule_id
        ).first()

    @classmethod
    def find_by_grade_schedule_id_and_student_id_and_type(
        cls, grade_schedule: GradeSchedule, student: Student, type: AttendanceTypeEnum
    ):
        return cls.query.filter_by(
            student_id=student.id, grade_schedule_id=grade_schedule.id, type=type
        ).first()
    
    @classmethod
    def find_by_grade_schedule_and_type_and_student_ids(
        cls, grade_schedule: GradeSchedule, type: AttendanceTypeEnum, student_ids: list
    ):
        return cls.query.filter_by(
            grade_schedule_id=grade_schedule.id, type=type
        ).filter(cls.student_id.in_(student_ids)).all()
    
    def to_dict(self):
        return dict(
            student_id=self.student_id,
            grade_schedule_id=self.grade_schedule_id,
            type=self.type.value,
            status=self.status.value,
            is_notified_absence=self.is_notified_absence,
            note=self.note,
            check_time=self.check_time
        )
