from sqlalchemy import Column, Numeric, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from .base import db
from . import Student, Exam


class ExamScore(db.Model):
    __tablename__ = "exams_scores"
    __table_args__ = (db.PrimaryKeyConstraint("student_id", "exam_id"),)

    student_id = Column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
    exam_id = Column(
        Integer,
        ForeignKey("exams.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
    score = Column(Numeric, nullable=False)

    # relationship
    student = db.relationship("Student", backref="exams_scores")

    def to_dict(self):
        return dict(
            student=self.student.to_dict(), exam=self.exam.to_dict(), score=self.score
        )

    @classmethod
    def create_default(cls, exam: Exam, student: Student) -> "ExamScore":
        return cls(
            student_id=student.id,
            exam_id=exam.id,
            student=student,
            exam=exam,
            score=None,
        )

    @classmethod
    def find_by_student_and_exam(cls, student: Student, exam: Exam) -> "ExamScore":
        return cls.query.filter_by(student_id=student.id, exam_id=exam.id).first()
