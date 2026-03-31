from sqlalchemy import Integer, Text, Enum, ForeignKey, Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID

from ..helpers.enums import StudyYearResultEnum, RankingInUnitEnum

from .base import db


class StudyYearResult(db.Model):
    __tablename__ = "study_year_results"
    __table_args__ = (PrimaryKeyConstraint("student_id", "study_year_id"),)

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
    )
    study_year_id = Column(
        Integer,
        ForeignKey("study_years.id", ondelete="cascade", onupdate="cascade"),
    )
    remark = Column(Text)
    result = Column(Enum(StudyYearResultEnum))
    unit_ranking = Column(Enum(RankingInUnitEnum))
    notes = Column(Text)

    # relationship
    student = db.relationship("Student")
    study_year = db.relationship("StudyYear")

    @classmethod
    def get_by_student_and_study_year(cls, student_id, study_year_id) -> 'StudyYearResult':
        return cls.query.filter_by(student_id=student_id, study_year_id=study_year_id).first()
    
    @classmethod
    def create_default(cls, student_id, study_year_id) -> 'StudyYearResult':
        return cls(student_id=student_id, study_year_id=study_year_id)

    def to_dict(self):
        return dict(
            student_code=self.student.code,
            study_year_code=self.study_year.code,
            remark=self.remark,
            result=self.result.value if self.result else None,
            unit_ranking=self.unit_ranking.value if self.unit_ranking else None,
            notes=self.notes
        )
