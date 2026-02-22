from uuid import uuid4

from sqlalchemy import Column, String, Enum, Date, Boolean
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import List

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
    # address field
    address_city = Column(String(100))
    address_ward = Column(String(100))
    address_quarter = Column(String(100))
    address_street = Column(String(100))
    address_house_no = Column(String(100))
    is_old_address = Column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    old_address_city = Column(String(100))
    old_address_district = Column(String(100))
    old_address_ward = Column(String(100))
    old_address_quarter = Column(String(100))
    old_address_street = Column(String(100))
    old_address_house_no = Column(String(100))
    # parents info
    father_saint_name = Column(String(30))
    father_full_name = Column(String(100))
    father_job = Column(String(100))
    mother_saint_name = Column(String(30))
    mother_full_name = Column(String(100))
    mother_job = Column(String(100))

    # relationship
    # general_schedules: Mapped[List["GeneralSchedule"]] = relationship(
    #     back_populates="study_year", order_by="desc(GeneralSchedule.date)"
    # )
    contacts: Mapped[List["PersonalContactInfo"]] = relationship(
        back_populates="student"
    )

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
            address_city=self.address_city,
            address_ward=self.address_ward,
            address_quarter=self.address_quarter,
            address_street=self.address_street,
            address_house_no=self.address_house_no,
            is_old_address=self.is_old_address,
            old_address_city=self.old_address_city,
            old_address_district=self.old_address_district,
            old_address_ward=self.old_address_ward,
            old_address_quarter=self.old_address_quarter,
            old_address_street=self.old_address_street,
            old_address_house_no=self.old_address_house_no,
            father_saint_name=self.father_saint_name,
            father_full_name=self.father_full_name,
            father_job=self.father_job,
            mother_saint_name=self.mother_saint_name,
            mother_full_name=self.mother_full_name,
            mother_job=self.mother_job,
            contacts=[contact.to_dict() for contact in self.contacts],
        )
