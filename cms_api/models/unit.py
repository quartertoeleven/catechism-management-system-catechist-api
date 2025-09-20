from sqlalchemy import Column, String, Integer, ForeignKey

from .base import db


class Unit(db.Model):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    grade_id = Column(
        Integer,
        ForeignKey("grades.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
