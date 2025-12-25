from uuid import uuid4

from sqlalchemy import Column, String, Enum, Date
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
    date_of_birth = Column(Date)

    @classmethod
    def find_by_code(cls, code) -> "Student":
        return cls.query.filter_by(code=code).first()

    @property
    def full_name(self):
        full_name_arr = [self.last_name, self.middle_name, self.first_name]
        return " ".join(
            filter(
                lambda name_seg: name_seg is not None and name_seg.strip() != "",
                full_name_arr,
            )
        )

    @property
    def v1_qr_code_str(self):
        church_name = "Tam Hà"
        student_code = self.code
        full_name = self.full_name
        gender = "Nam" if self.gender == GenderEnum.MALE else "Nữ"
        return f"{church_name}|{student_code}|{full_name}|{gender}"

    def to_dict(self):
        return dict(
            code=self.code,
            saint_name=self.saint_name,
            last_name=self.last_name,
            middle_name=self.middle_name,
            first_name=self.first_name,
            full_name=self.full_name,
            gender=self.gender.value,
            date_of_birth=self.date_of_birth,
        )
