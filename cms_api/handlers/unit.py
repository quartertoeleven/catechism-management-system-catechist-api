from ..models import Unit, Catechist, StudyYear
from ..models.base import OperationResult

# def _get_unit_students(unit: Unit):
#     unit_students = unit.students
#     unit_student_dicts = [unit_student.to_dict() for unit_student in unit_students]

#     return OperationResult(success=True, message="Unit student found", data=unit_student_dicts)


def get_unit_list_for_a_catechist(catechist: Catechist, study_year_code: str):
    # For a catechist, get the list of units in the same grade as the catechist in a specific study year
    study_year = StudyYear.get_by_code(study_year_code)
    if study_year is None:
        return OperationResult(success=False, message="Study year not found")

    catechist = Catechist.find_by_id(catechist.id)
    if catechist is None:
        return OperationResult(success=False, message="Catechist not found")

    # Normally, in a study year, a catechist will only assigned 1 unit only
    # TODO: need to think about the "off-schedule" units later on
    catechist_current_unit = catechist.units.filter(
        Unit.grade_id == study_year.grade_id
    ).first()
    catechist_current_grade = catechist_current_unit.grade
    current_grade_units = catechist_current_grade.units

    all_unit_dicts = []

    for unit in current_grade_units:
        unit_dict = unit.to_dict()
        unit_dict["my_unit"] = (
            True if unit.code == catechist_current_unit.code else False
        )
        all_unit_dicts.append(unit_dict)

    return OperationResult(success=True, message="Unit list found", data=all_unit_dicts)


def get_unit_details(unit_code, include_students=False):
    unit = Unit.find_by_code(unit_code)

    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    unit_dict = unit.to_dict()

    if include_students:
        unit_dict["students"] = [student.to_dict() for student in unit.students]

    return OperationResult(success=True, message="Unit found", data=unit_dict)
