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
    is_baptized = Column(Boolean, nullable=False, default=True, server_default="true")
    baptism_date = Column(Date)
    baptism_place = Column(String(100))
    is_confirmed = Column(
        Boolean, nullable=False, default=False, server_default="false"
    )
    confirmation_date = Column(Date)
    confirmation_place = Column(String(100))
    # address field
    address_line_1 = Column(String(100))
    address_line_2 = Column(String(100))
    old_address_line_1 = Column(String(100))
    old_address_line_2 = Column(String(100))
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

    def to_dict(self, with_group=False):
        if not with_group:
            return dict(
                code=self.code,
                saint_name=self.saint_name,
                last_name=self.last_name,
                middle_name=self.middle_name,
                first_name=self.first_name,
                full_name=self.full_name,
                gender=self.gender.value,
                date_of_birth=self.date_of_birth,
                is_baptized=self.is_baptized,
                baptism_date=self.baptism_date,
                baptism_place=self.baptism_place,
                is_confirmed=self.is_confirmed,
                confirmation_date=self.confirmation_date,
                confirmation_place=self.confirmation_place,
                address_line_1=self.address_line_1,
                address_line_2=self.address_line_2,
                old_address_line_1=self.old_address_line_1,
                old_address_line_2=self.old_address_line_2,
                father_saint_name=self.father_saint_name,
                father_full_name=self.father_full_name,
                father_job=self.father_job,
                mother_saint_name=self.mother_saint_name,
                mother_full_name=self.mother_full_name,
                mother_job=self.mother_job,
                contacts=[contact.to_dict() for contact in self.contacts],
            )
        else:
            return dict(
                basic=dict(
                    code=self.code,
                    saint_name=self.saint_name,
                    last_name=self.last_name,
                    middle_name=self.middle_name,
                    first_name=self.first_name,
                    full_name=self.full_name,
                    gender=self.gender.value,
                    date_of_birth=self.date_of_birth,
                ),
                sacraments=dict(
                    is_baptized=self.is_baptized,
                    baptism_date=self.baptism_date,
                    baptism_place=self.baptism_place,
                    is_confirmed=self.is_confirmed,
                    confirmation_date=self.confirmation_date,
                    confirmation_place=self.confirmation_place,
                ),
                parents=dict(
                    father_saint_name=self.father_saint_name,
                    father_full_name=self.father_full_name,
                    father_job=self.father_job,
                    mother_saint_name=self.mother_saint_name,
                    mother_full_name=self.mother_full_name,
                    mother_job=self.mother_job,
                ),
                address=dict(
                    address_line_1=self.address_line_1,
                    address_line_2=self.address_line_2,
                    old_address_line_1=self.old_address_line_1,
                    old_address_line_2=self.old_address_line_2,
                ),
                contacts=[contact.to_dict() for contact in self.contacts],
            )
