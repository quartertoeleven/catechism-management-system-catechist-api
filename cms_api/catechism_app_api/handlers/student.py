from cms_api.models.base import OperationResult, db
from cms_api.models import Student, ExamScore, Exam, PersonalContactInfo, StudyYear, StudyYearResult
from cms_api.helpers.enums import (
    GenderEnum,
    ContactInfoTypeEnum,
    ContactRelationTypeEnum,
    RankingInUnitEnum,
    StudyYearResultEnum
)


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
        student.baptism_date = (
            sacrament_info.get("baptism_date") if student.is_baptized else None
        )
        student.baptism_place = (
            sacrament_info.get("baptism_place") if student.is_baptized else None
        )
        student.is_confirmed = sacrament_info.get("is_confirmed")
        student.confirmation_date = (
            sacrament_info.get("confirmation_date") if student.is_confirmed else None
        )
        student.confirmation_place = (
            sacrament_info.get("confirmation_place") if student.is_confirmed else None
        )

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


def create_or_update_student_contacts(student_code, contact_dict):
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    if contact_dict.get("id") is None:
        # This is a new contact
        new_contact = PersonalContactInfo(
            student_id=student.id,
            type=ContactInfoTypeEnum(contact_dict.get("type")),
            relationship=(
                ContactRelationTypeEnum(contact_dict.get("relationship"))
                if contact_dict.get("relationship") is not None
                else None
            ),
            info=contact_dict.get("info"),
        )
        db.session.add(new_contact)
    else:
        # This is an existing contact. Update info
        existing_contact = db.session.get(PersonalContactInfo, contact_dict.get("id"))
        if existing_contact is None:
            return OperationResult(success=False, message="Contact not found")
        existing_contact.type = ContactInfoTypeEnum(contact_dict.get("type"))
        existing_contact.relationship = (
            ContactRelationTypeEnum(contact_dict.get("relationship"))
            if contact_dict.get("relationship") is not None
            else None
        )

        existing_contact.info = contact_dict.get("info")

    db.session.flush()

    return OperationResult(
        success=True,
        message="Thêm liên lạc thành công",
        data=student.to_dict(True).get("contacts"),
    )


def delete_student_contact(student_code, contact_id):
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    existing_contact = db.session.get(PersonalContactInfo, contact_id)

    if existing_contact is None or existing_contact.student_id != student.id:
        return OperationResult(success=False, message="Contact not found")

    db.session.delete(existing_contact)
    db.session.flush()

    return OperationResult(
        success=True,
        message="Xóa liên lạc thành công",
        data=student.to_dict(True).get("contacts"),
    )

def update_student_year_end_result(student_code, year_end_result_dict):
    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")
    
    # Get the current year end result
    study_year_code = year_end_result_dict.get("study_year_code")
    study_year: StudyYear

    if study_year_code is None:
        study_year = StudyYear.get_current_study_year()
    else:
        study_year = StudyYear.get_by_code(study_year_code)
    
    if study_year is None:
        return OperationResult(success=False, message="Study year not found")
    
    existing_result = StudyYearResult.get_by_student_and_study_year(student.id, study_year.id)
    
    if existing_result is None:
        new_result = StudyYearResult.create_default(student.id, study_year.id)
        new_result.remark = year_end_result_dict.get("remark")
        new_result.result = StudyYearResultEnum(year_end_result_dict.get("result")) if year_end_result_dict.get("result") else None
        new_result.unit_ranking = RankingInUnitEnum(year_end_result_dict.get("unit_ranking")) if year_end_result_dict.get("unit_ranking") else None
        new_result.notes = year_end_result_dict.get("notes")
        db.session.add(new_result)
    else:
        # Update the year end result
        existing_result.remark = year_end_result_dict.get("remark")
        existing_result.result = StudyYearResultEnum(year_end_result_dict.get("result")) if year_end_result_dict.get("result") else None
        existing_result.unit_ranking = RankingInUnitEnum(year_end_result_dict.get("unit_ranking")) if year_end_result_dict.get("unit_ranking") else None
        existing_result.notes = year_end_result_dict.get("notes")
    
    db.session.flush()

    return OperationResult(success=True, message="Cập nhật kết quả cuối năm thành công")
