from sqlalchemy import Column, String, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped

from ..helpers.enums import ContactInfoTypeEnum, ContactRelationTypeEnum
from .base import db
from . import Student, Catechist


class PersonalContactInfo(db.Model):
    __tablename__ = "personal_contact_infos"

    id = Column(Integer, primary_key=True)
    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
        nullable=True,
    )

    catechist_id = Column(
        UUID(as_uuid=True),
        ForeignKey("catechists.id", ondelete="cascade", onupdate="cascade"),
        nullable=True,
    )
    relationship = Column(Enum(ContactRelationTypeEnum), nullable=True)
    type = Column(Enum(ContactInfoTypeEnum), nullable=False)
    info = Column(String(100), nullable=False)

    # relationship
    student: Mapped["Student"] = db.relationship(
        "Student", back_populates="contacts", lazy="subquery"
    )
    catechist: Mapped["Catechist"] = db.relationship(
        "Catechist", back_populates="contacts", lazy="subquery"
    )

    def to_dict(self):
        return dict(
            id=self.id,
            relationship=self.relationship.value,
            type=self.type.value,
            info=self.info,
        )
