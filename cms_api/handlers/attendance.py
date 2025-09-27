from ..helpers.enums import AttendanceTypeEnum, AttendanceStatusEnum

from ..models import Student, StudentAttendance, GradeSchedule, OperationResult
from ..models.base import db


def __create_new_student_attendance_with_default_values(
    grade_schedule: GradeSchedule, student: Student, type: AttendanceTypeEnum
):
    return StudentAttendance(
        student_id=student.id,
        grade_schedule_id=grade_schedule.id,
        type=type,
        status=AttendanceStatusEnum.ABSENT,
        is_notified_absence=False,
    )


def __create_or_update_student_attendance(
    grade_schedule: GradeSchedule,
    student: Student,
    attendance_type: AttendanceTypeEnum,
    attendance_status: AttendanceStatusEnum,
    is_notified_absence: bool,
):
    attendance_entry = StudentAttendance.find_by_grade_schedule_id_and_student_id_and_type(
        grade_schedule, student, attendance_type
    )

    if attendance_entry is None:
        attendance_entry = __create_new_student_attendance_with_default_values(
            grade_schedule, student, attendance_type
        )

        db.session.add(attendance_entry)
    
    attendance_entry.status = attendance_status
    if attendance_status == AttendanceStatusEnum.PRESENT:
        attendance_entry.is_notified_absence = None
    else:
        attendance_entry.is_notified_absence = is_notified_absence


def handle_attendance_check(grade_schedule_id, attendance_check_dict) -> OperationResult:
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

    return OperationResult(success=True, message="Attendance checked done")

    # type = attendance_check_dict.get('type')
    # student_id = attendance_check_dict.get('student_id')
    # if type == AttendanceType.MASS:
    #     return "mass"
    # elif type == AttendanceType.LESSON:
    #     return "lesson"
