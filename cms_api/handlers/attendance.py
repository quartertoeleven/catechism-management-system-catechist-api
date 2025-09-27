from ..helpers.enums import AttendanceTypeEnum, AttendanceStatusEnum

from ..models import Student, StudentAttendance, GradeSchedule, OperationResult
from ..models.base import db


def __create_new_student_attendance_with_default_values(
    grade_schedule: GradeSchedule, student: Student
):
    return StudentAttendance(
        student_id=student.id,
        grade_schedule_id=grade_schedule.id,
        mass_status=AttendanceStatusEnum.ABSENT,
        is_mass_absence_notified=False,
        lesson_status=AttendanceStatusEnum.ABSENT,
        is_lesson_absence_notified=False,
    )


def __create_or_update_student_attendance(
    grade_schedule: GradeSchedule,
    student: Student,
    attendance_type: AttendanceTypeEnum,
    attendance_status: AttendanceStatusEnum,
    is_absence_notified: bool,
):
    attendance_entry = StudentAttendance.find_by_grade_schedule_id_and_student_id(
        grade_schedule.id, student.id
    )
    if attendance_entry is None:
        attendance_entry = __create_new_student_attendance_with_default_values(
            grade_schedule, student
        )

        db.session.add(attendance_entry)

    match attendance_type:
        case AttendanceTypeEnum.MASS:
            attendance_entry.mass_status = attendance_status
            if attendance_status == AttendanceStatusEnum.PRESENT:
                attendance_entry.is_mass_absence_notified = None
                attendance_entry.mass_absence_reason = None
            else:
                attendance_entry.is_mass_absence_notified = is_absence_notified
        case AttendanceTypeEnum.LESSON:
            attendance_entry.lesson_status = attendance_status
            if attendance_status == AttendanceStatusEnum.PRESENT:
                attendance_entry.is_lesson_absence_notified = None
                attendance_entry.lesson_absence_reason = None
            else:
                attendance_entry.is_mass_absence_notified = is_absence_notified


def handle_attendance_check(attendance_check_dict):
    student_code = attendance_check_dict.get("student_code")
    grade_schedule_id = attendance_check_dict.get("grade_schedule_id")
    type = attendance_check_dict.get("type")
    status = attendance_check_dict.get("status")
    is_absence_notified = attendance_check_dict.get("is_absence_notified")

    student = Student.find_by_code(student_code)
    if student is None:
        return OperationResult(success=False, message="Student not found")

    grade_schedule = GradeSchedule.find_by_id(grade_schedule_id)
    if grade_schedule is None:
        return OperationResult(success=False, message="Grade schedule not found")
    
    type_enum = AttendanceTypeEnum(type)
    status_enum = AttendanceStatusEnum(status)

    __create_or_update_student_attendance(
        grade_schedule,
        student,
        type_enum,
        status_enum,
        is_absence_notified
    )

    # type = attendance_check_dict.get('type')
    # student_id = attendance_check_dict.get('student_id')
    # if type == AttendanceType.MASS:
    #     return "mass"
    # elif type == AttendanceType.LESSON:
    #     return "lesson"
