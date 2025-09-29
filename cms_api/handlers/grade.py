from ..models import Grade, GradeSchedule
from ..models.base import OperationResult


def get_grade_schedules(grade_code):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    all_schedules = GradeSchedule.get_schedules_for_grade(grade)
    all_schedules_as_dict = [schedule.to_dict() for schedule in all_schedules]

    return OperationResult(
        success=True, message="Grade schedule found", data=all_schedules_as_dict
    )


def get_grade_units(grade_code):
    grade = Grade.get_by_code(grade_code)

    if grade is None:
        return OperationResult(success=False, message="Grade not found")

    all_units = grade.units
    all_units_as_dict = [unit.to_dict() for unit in all_units]

    return OperationResult(
        success=True, message="Grade units found", data=all_units_as_dict
    )
