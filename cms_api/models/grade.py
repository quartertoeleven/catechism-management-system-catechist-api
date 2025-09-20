from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import db


class Grade(db.Model):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    head_catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"),
    )
    head_assistant_catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"),
    )
    accountant_catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="set null", onupdate="cascade"),
    )
    study_year_id = Column(
        Integer,
        ForeignKey("study_years.id", ondelete="set null", onupdate="cascade"),
        nullable=False,
    )
