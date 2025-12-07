from cms_api.helpers.enums import AttendanceTypeEnum, AttendanceStatusEnum
from cms_api.helpers.qr_helpers import get_student_code_from_qr

from ...models import Student, StudentAttendance, GradeSchedule, StudyYear, UnitStudent
from ...models.base import db, OperationResult


def __create_or_update_student_attendance(
    grade_schedule: GradeSchedule,
    student: Student,
    attendance_type: AttendanceTypeEnum,
    attendance_status: AttendanceStatusEnum,
    is_notified_absence: bool,
):
    attendance_entry = (
        StudentAttendance.find_by_grade_schedule_id_and_student_id_and_type(
            grade_schedule, student, attendance_type
        )
    )

    if attendance_entry is None:
        attendance_entry = StudentAttendance.create_default(
            grade_schedule, student, attendance_type
        )

        db.session.add(attendance_entry)

    attendance_entry.status = attendance_status
    if attendance_status == AttendanceStatusEnum.PRESENT:
        attendance_entry.is_notified_absence = None
    else:
        attendance_entry.is_notified_absence = is_notified_absence


def handle_attendance_check(
    grade_schedule_id, attendance_check_dict
) -> OperationResult:
    student_code = attendance_check_dict.get("student_code")
    type = attendance_check_dict.get("type")
    status = attendance_check_dict.get("status")
    is_notified_absence = attendance_check_dict.get("is_notified_absence")

    student = Student.find_by_code(student_code)
    if student is None:
        return OperationResult(success=False, message="Student not found")

    grade_schedule = GradeSchedule.find_by_id(grade_schedule_id)
    if grade_schedule is None:
        return OperationResult(success=False, message="Grade schedule not found")

    type_enum = AttendanceTypeEnum(type)
    status_enum = AttendanceStatusEnum(status)

    __create_or_update_student_attendance(
        grade_schedule, student, type_enum, status_enum, is_notified_absence
    )

    result_dict = dict(
        student=dict(
            code=student.code,
            fullname=student.full_name,
            saint_name=student.saint_name,
        )
    )

    return OperationResult(
        success=True, message="Attendance checked done", data=result_dict
    )


def handle_attendance_check_using_qr(
    grade_schedule_id, attendance_check_dict_with_qr
) -> OperationResult:
    raw_str_from_qr = attendance_check_dict_with_qr.get("qrData")
    student_code = get_student_code_from_qr(raw_str_from_qr)
    if student_code is None:
        return OperationResult(success=False, message="QR data not valid")

    attendance_check_dict = dict(
        student_code=student_code,
        type=attendance_check_dict_with_qr.get("type"),
        status=AttendanceStatusEnum.PRESENT.value,
        is_notified_absence=None,
    )

    return handle_attendance_check(grade_schedule_id, attendance_check_dict)
