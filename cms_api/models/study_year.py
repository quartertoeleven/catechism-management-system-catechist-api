from sqlalchemy import Column, String, Integer, Boolean

from .base import db


class StudyYear(db.Model):
    __tablename__ = "study_years"

    id = Column(Integer, primary_key=True)
    code = Column(String(10), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    main_subject = Column(String(100))
    is_current = Column(Boolean, nullable=False, default=False, server_default="false")

    @classmethod
    def get_by_code(cls, code) -> "StudyYear":
        return cls.query.filter_by(code=code).first()
    
    @classmethod
    def get_current(cls) -> "StudyYear":
        return cls.query.filter_by(is_current=True).first()
