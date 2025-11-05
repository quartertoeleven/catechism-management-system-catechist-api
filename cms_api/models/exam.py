from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from .base import db
from ..helpers.enums import SemesterEnum

class Exam(db.Model):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    factor = Column(Integer, nullable=False, default=1, server_default="1")
    semester = semester = Column(Enum(SemesterEnum), nullable=False)
    grade_id = Column(
        ForeignKey("grades.id", ondelete="cascade", onupdate="cascade"), nullable=False
    )
    
    # relationship
    grade = db.relationship("Grade", backref="exams")

    @classmethod
    def find_by_id(cls, id) -> 'Exam':
        return cls.query.get(id)

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            factor=self.factor,
            semester=self.semester,
            grade_id=self.grade_id
        )




    
