from uuid import uuid4

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID

from .base import db
from ..helpers.enums import TitleEnum, GenderEnum


class Catechist(db.Model):
    __tablename__ = "catechists"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=db.func.gen_random_uuid(),
    )
    title = Column(Enum(TitleEnum), nullable=False)
    saint_name = Column(String(30), nullable=False)
    last_name = Column(String(20), nullable=False)
    middle_name = Column(String(30))
    first_name = Column(String(30), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)

    # relationship
    units = db.relationship("Unit", secondary="unit_catechists", order_by="Unit.code")

    @classmethod
    def find_by_id(cls, id) -> "Catechist":
        return cls.query.filter_by(id=id).first()

    def to_dict(self):
        return dict(
            title=self.title,
            saint_name=self.saint_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            first_name=self.first_name,
            gender=self.gender,
        )
