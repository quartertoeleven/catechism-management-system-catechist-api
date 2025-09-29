from sqlalchemy import Integer, ForeignKey, Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from .base import db


class UnitCatechist(db.Model):
    __tablename__ = "unit_catechists"
    __table_args__ = (PrimaryKeyConstraint("catechist_id", "unit_id"),)

    catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="cascade", onupdate="cascade"),
    )
    unit_id = Column(
        Integer,
        ForeignKey("units.id", ondelete="cascade", onupdate="cascade"),
    )
