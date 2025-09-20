from uuid import uuid4

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID

from .base import db
from ..helpers.enums import GenderEnum

class Student(db.Model):
    __tablename__ = "students"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        server_default=db.func.gen_random_uuid(),
    )
    code = Column(String(20), nullable=False, unique=True, index=True)
    saint_name = Column(String(30), nullable=False)
    last_name = Column(String(20), nullable=False)
    middle_name = Column(String(30))
    first_name = Column(String(30), nullable=False)
    gender = Column(Enum(GenderEnum), nullable=False)

