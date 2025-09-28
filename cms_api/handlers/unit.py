from ..models import Unit, OperationResult

# def _get_unit_students(unit: Unit):
#     unit_students = unit.students
#     unit_student_dicts = [unit_student.to_dict() for unit_student in unit_students]

#     return OperationResult(success=True, message="Unit student found", data=unit_student_dicts)

def get_unit_details(unit_code, include_students=False):
    unit = Unit.find_by_code(unit_code)

    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    unit_dict = unit.to_dict()

    if include_students:
        unit_dict["students"] = [student.to_dict() for student in unit.students]

    return OperationResult(success=True, message="Unit found", data=unit_dict)
    