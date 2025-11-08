from cms_api.models.base import OperationResult, db
from cms_api.models import Student, ExamScore, Exam


def create_or_update_student_exam_score(student_code, exam_id, score):
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    exam = Exam.find_by_id(exam_id)

    if exam is None:
        return OperationResult(success=False, message="Exam not found")

    examScore = ExamScore.find_by_student_and_exam(student, exam)

    if examScore is None:
        newExamScore = ExamScore.create_default(exam, student)
        newExamScore.score = score
        db.session.add(newExamScore)
    else:
        examScore.score = score

    db.session.flush()

    return OperationResult(success=True, message="Student exam score updated")
