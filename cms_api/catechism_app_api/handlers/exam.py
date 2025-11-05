from cms_api.models.base import OperationResult,db
from cms_api.models import Exam, Grade
from cms_api.helpers.enums import SemesterEnum

def create_or_update_exam(exam_dict):
    grade_code = exam_dict.get("grade_code")
    
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    if exam_dict.get("id") is not None:
        existing_exam = Exam.find_by_id(exam_dict.get("id"))
        if existing_exam is None:
            return OperationResult(success=False, message="Exam not found")

        existing_exam.name = exam_dict.get("name")
        existing_exam.factor = exam_dict.get("factor")
        existing_exam.semester = SemesterEnum(exam_dict.get("semester"))

        db.session.flush()

        return OperationResult(success=True, message="Exam details updated", data=existing_exam.to_dict())
    
    new_exam = Exam(
        name=exam_dict.get("name"),
        factor=exam_dict.get("factor"),
        semester=SemesterEnum(exam_dict.get("semester")),
        grade_id=grade.id
    )

    db.session.add(new_exam)
    db.session.flush()

    return OperationResult(success=True, message="Exam created", data=new_exam.to_dict())
