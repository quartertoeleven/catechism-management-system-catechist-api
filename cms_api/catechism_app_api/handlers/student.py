from cms_api.models.base import OperationResult, db
from cms_api.models import Student, ExamScore, Exam
from cms_api.helpers.enums import GenderEnum


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


def get_student_details(student_code):
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    return OperationResult(
        success=True, message="Student found", data=student.to_dict(True)
    )


def update_student_details(student_code, updated_info_dict):
    # updated_info_dict can contains all or some of the following keys:
    # basic: contains basic info
    # parents: contains info about the student parents
    # sacraments: contains info about the baptism and confirmation
    # address: contains info about the address
    # contacts: contains a list of contacts related to the student
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    # update basic info
    if "basic" in updated_info_dict.keys():
        basic_info = updated_info_dict.get("basic")
        student.saint_name = basic_info.get("saint_name")
        student.last_name = basic_info.get("last_name")
        student.middle_name = basic_info.get("middle_name")
        student.first_name = basic_info.get("first_name")
        student.gender = GenderEnum(basic_info.get("gender"))
        student.date_of_birth = basic_info.get("date_of_birth")

    if "sacraments" in updated_info_dict.keys():
        sacrament_info = updated_info_dict.get("sacraments")
        student.is_baptized = sacrament_info.get("is_baptized")
        student.baptism_date = sacrament_info.get("baptism_date") if student.is_baptized else None
        student.baptism_place = sacrament_info.get("baptism_place") if student.is_baptized else None
        student.is_confirmed = sacrament_info.get("is_confirmed")
        student.confirmation_date = sacrament_info.get("confirmation_date") if student.is_confirmed else None
        student.confirmation_place = sacrament_info.get("confirmation_place") if student.is_confirmed else None
    
    if "parents" in updated_info_dict.keys():
        parents_info = updated_info_dict.get("parents")
        student.father_saint_name = parents_info.get("father_saint_name")
        student.father_full_name = parents_info.get("father_full_name")
        student.father_job = parents_info.get("father_job")
        student.mother_saint_name = parents_info.get("mother_saint_name")
        student.mother_full_name = parents_info.get("mother_full_name")
        student.mother_job = parents_info.get("mother_job")

    if "address" in updated_info_dict.keys():
        address_info = updated_info_dict.get("address")
        student.address_line_1 = address_info.get("address_line_1")
        student.address_line_2 = address_info.get("address_line_2")
        student.old_address_line_1 = address_info.get("old_address_line_1")
        student.old_address_line_2 = address_info.get("old_address_line_2")

    db.session.flush()

    return OperationResult(success=True, message="Cập nhật thông tin thành công")
