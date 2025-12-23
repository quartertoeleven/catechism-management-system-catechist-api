from cms_api.models.base import db
from cms_api.helpers.enums import SemesterEnum

from ...models import Grade, GradeSchedule, GeneralSchedule
from ...models.base import OperationResult


def get_grade_schedules(grade_code):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    all_schedules = GradeSchedule.get_schedules_for_grade(grade)
    all_schedules_as_dict = [schedule.to_dict() for schedule in all_schedules]

    return OperationResult(
        success=True,
        message="Grade schedule found",
        data=dict(grade_details=grade.to_dict(), schedules=all_schedules_as_dict),
    )


def get_specific_grade_schedule(schedule_id):
    schedule = GradeSchedule.find_by_id(schedule_id)

    if schedule is None:
        return OperationResult(success=False, message="Schedule not found")

    return OperationResult(
        success=True, message="Schedule found", data=schedule.to_dict()
    )


def create_or_update_grade_schedule(grade_code, schedule_dict):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    current_grade_schedule: GradeSchedule

    if schedule_dict.get("id"):
        current_grade_schedule = GradeSchedule.find_by_id(schedule_dict.get("id"))

        if current_grade_schedule is None:
            return OperationResult(success=False, message="Grade schedule not found")

        if current_grade_schedule.grade_id != grade.id:
            return OperationResult(
                success=False, message="Cannot edit schedule of other grade"
            )

    else:
        current_grade_schedule = GradeSchedule(
            semester=(
                SemesterEnum(schedule_dict.get("semester"))
                if schedule_dict.get("semester") is not None
                else None
            ),
            date=schedule_dict.get("date"),
            mass_content=schedule_dict.get("mass_content"),
            is_mass_attendance_check=schedule_dict.get("is_mass_attendance_check"),
            lesson_conteent=schedule_dict.get("lesson_content"),
            is_lesson_attenance_check=schedule_dict.get("is_lesson_attendance_check"),
            grade_id=grade.id,
        )

    # aligning the grade schedule with general schedule for empty information
    if schedule_dict.get("general_schedule_id") is not None:
        general_schedule = GeneralSchedule.find_by_id(
            schedule_dict.get("general_schedule_id")
        )

        if general_schedule is None:
            return OperationResult(success=False, message="General schedule not found")

        if current_grade_schedule.semester is None:
            current_grade_schedule.semester = general_schedule.semester
        if current_grade_schedule.date is None:
            current_grade_schedule.date = general_schedule.date
        if (
            current_grade_schedule.mass_content is None
            or not current_grade_schedule.mass_content.strip()
        ):
            current_grade_schedule.mass_content = general_schedule.mass_content
        if current_grade_schedule.is_mass_attendance_check is None:
            current_grade_schedule.is_mass_attendance_check = (
                general_schedule.is_mass_attendance_check
            )
        if (
            current_grade_schedule.lesson_content is None
            or not current_grade_schedule.lesson_content.strip()
        ):
            current_grade_schedule.lesson_content = general_schedule.lesson_content
        if current_grade_schedule.is_lesson_attendance_check is None:
            current_grade_schedule.is_lesson_attendance_check = (
                general_schedule.is_lesson_attendance_check
            )

    db.session.add(current_grade_schedule)
    db.session.flush()

    return OperationResult(
        success=True,
        message="Grade schedule created",
        data=current_grade_schedule.to_dict(),
    )


def delete_grade_schedule(grade_code, schedule_id):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    existing_grade_schedule = GradeSchedule.find_by_id(schedule_id)

    if existing_grade_schedule is None:
        return OperationResult(success=False, message="Grade schedule not found")

    if existing_grade_schedule.grade_id != grade.id:
        return OperationResult(
            success=False, message="Cannot delete schedule of the other grade"
        )

    db.session.delete(existing_grade_schedule)
    db.session.flush()

    return OperationResult(success=True, message="Grade schedule deleted")


def get_grade_units(grade_code):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    all_units = grade.units
    all_units_as_dict = [unit.to_dict() for unit in all_units]

    return OperationResult(
        success=True, message="Grade units found", data=all_units_as_dict
    )


def get_grade_exams(grade_code):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    result = dict(grade_details=grade.to_dict(), exams=[])

    all_exams = grade.exams
    result["exams"] = [test.to_dict() for test in all_exams]

    return OperationResult(success=True, message="Grade exams found", data=result)
