from sqlalchemy import Column, String, Integer, ForeignKey

from .base import db


class Unit(db.Model):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False, unique=True, index=True)
    name = Column(String(100), nullable=False)
    grade_id = Column(
        Integer,
        ForeignKey("grades.id", ondelete="cascade", onupdate="cascade"),
        nullable=False,
    )
    # relationship
    students = db.relationship(
        "Student", secondary="unit_students", order_by="Student.first_name"
    )
    catechists = db.relationship(
        "Catechist",
        secondary="unit_catechists",
        order_by="Catechist.first_name",
        back_populates="units",
    )
    grade = db.relationship("Grade", backref="units")

    @classmethod
    def find_by_code(cls, unit_code) -> "Unit":
        return cls.query.filter_by(code=unit_code).first()

    def to_dict(self):
        return dict(code=self.code, name=self.name, grade_code=self.grade.code)
