from sqlalchemy import Integer, ForeignKey, Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import db

class UnitStudent(db.Model):
    __tablename__ = "unit_students"
    __table_args__ = (PrimaryKeyConstraint("student_id", "unit_id"), )

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
    )
    unit_id = Column(
        Integer,
        ForeignKey("units.id", ondelete="cascade", onupdate="cascade"),
    )
