from sqlalchemy import Column, String, Integer

from .base import db


class StudyYear(db.Model):
    __tablename__ = "study_years"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    main_subject = Column(String(100))

    @classmethod
    def get_by_code(cls, code) -> "StudyYear":
        return cls.query.filter_by(code=code).first()
