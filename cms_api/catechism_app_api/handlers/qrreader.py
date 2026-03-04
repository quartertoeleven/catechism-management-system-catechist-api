from cms_api.helpers.qr_helpers import get_student_code_from_qr

from ...models import Student
from ...models.base import OperationResult

def read_student_qr_code(raw_str_from_qr) -> OperationResult:
    student_code = get_student_code_from_qr(raw_str_from_qr)
    if student_code is None:
        return OperationResult(success=False, message="QR data not valid")
    
    student = Student.find_by_code(student_code)
    
    if student is None:
        return OperationResult(success=False, message="Student not found")
    
    return OperationResult(
        success=True, message="", data=student.to_dict()
    )
