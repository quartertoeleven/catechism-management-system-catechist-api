from cms_api.helpers.qr_helpers import get_student_code_from_qr

from ...models import Student, StudyYear, Unit, UnitStudent
from ...models.base import OperationResult

def read_student_qr_code(raw_str_from_qr) -> OperationResult:
    student_code = get_student_code_from_qr(raw_str_from_qr)
    if student_code is None:
        return OperationResult(success=False, message="Mã QR không đúng định dạng")
    
    student = Student.find_by_code(student_code)
    
    if student is None:
        return OperationResult(success=False, message="Không tìm thấy học viên")
    
    current_study_year = StudyYear.get_current()
    all_grades_id = [grade.id for grade in current_study_year.grades]
    all_units = Unit.query.filter(Unit.grade_id.in_(all_grades_id)).all()
    all_units_id = [unit.id for unit in all_units]

    current_unit_student = UnitStudent.query.filter(
        UnitStudent.student_id == student.id,
        UnitStudent.unit_id.in_(all_units_id)
    ).first()

    current_unit = None
    if current_unit_student is not None:
        current_unit = Unit.query.get(current_unit_student.unit_id)
    
    response_data = student.to_dict()
    response_data['current_unit'] = current_unit.to_dict() if current_unit is not None else None

    return OperationResult(
        success=True, message="", data=response_data
    )
