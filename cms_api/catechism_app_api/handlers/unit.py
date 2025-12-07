from ...models import (
    Unit,
    Catechist,
    StudyYear,
    GradeSchedule,
    Student,
    StudentAttendance,
    Exam,
    ExamScore,
)
from ...models.base import OperationResult, db
from ...helpers.enums import AttendanceTypeEnum

# def _get_unit_students(unit: Unit):
#     unit_students = unit.students
#     unit_student_dicts = [unit_student.to_dict() for unit_student in unit_students]

#     return OperationResult(success=True, message="Unit student found", data=unit_student_dicts)


def get_unit_list_for_a_catechist(catechist: Catechist, study_year_code: str):
    # For a catechist, get the list of units in the same grade as the catechist in a specific study year
    study_year: StudyYear

    if study_year_code is None:
        study_year = StudyYear.get_current()
    else:
        study_year = StudyYear.get_by_code(study_year_code)
        if study_year is None:
            return OperationResult(success=False, message="Study year not found")

    catechist = Catechist.find_by_id(catechist.id)
    if catechist is None:
        return OperationResult(success=False, message="Catechist not found")

    # Normally, in a study year, a catechist will only assigned 1 unit only
    # TODO: need to think about the "off-schedule" units later on
    all_unit_dicts = []

    if len(catechist.units) > 0:
        catechist_current_unit = list(
            filter(
                lambda unit: unit.grade.study_year_id == study_year.id, catechist.units
            )
        )[0]
        catechist_current_grade = catechist_current_unit.grade
        current_grade_units = catechist_current_grade.units

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


def get_unit_schedule(unit_code):
    unit = Unit.find_by_code(unit_code)

    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    all_schedules = GradeSchedule.get_schedules_for_grade(unit.grade)
    all_schedules_as_dict = [schedule.to_dict() for schedule in all_schedules]

    result = dict(schedules=all_schedules_as_dict, unit_info=unit.to_dict())

    return OperationResult(success=True, message="Unit schedule found", data=result)


def get_unit_attendances_for_schedule(
    unit_code: str, grade_schedule_id: int, type: str
):
    attendance_type = AttendanceTypeEnum(type)
    if attendance_type is None:
        return OperationResult(success=False, message="Attendance type not found")

    unit = Unit.find_by_code(unit_code)
    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    grade_schedule = GradeSchedule.find_by_id(grade_schedule_id)
    if grade_schedule is None:
        return OperationResult(success=False, message="Grade schedule not found")

    unit_students = unit.students
    unit_student_ids = [unit_student.id for unit_student in unit_students]

    student_attendance_list = (
        StudentAttendance.find_by_grade_schedule_and_type_and_student_ids(
            grade_schedule, attendance_type, unit_student_ids
        )
    )

    result = []

    for student in unit_students:
        existing_attendance_entry = next(
            (
                student_attendance
                for student_attendance in student_attendance_list
                if student_attendance.student_id == student.id
            ),
            None,
        )
        if existing_attendance_entry is None:
            default_attendance_entry = StudentAttendance.create_default(
                grade_schedule, student, attendance_type
            )
            result.append(default_attendance_entry.to_dict())
        else:
            result.append(existing_attendance_entry.to_dict())

    return OperationResult(success=True, message="Unit attendances found", data=result)


def get_unit_attendances_report(unit_code: str):
    unit = Unit.find_by_code(unit_code)
    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    grade_schedules = GradeSchedule.get_schedules_for_grade(unit.grade)
    grade_schedules_ids = [grade_schedule.id for grade_schedule in grade_schedules]

    unit_students = unit.students
    unit_student_ids = [unit_student.id for unit_student in unit_students]

    student_attendance_list = (
        StudentAttendance.find_by_student_ids_and_grade_schedule_ids(
            unit_student_ids, grade_schedules_ids
        )
    )

    result = []

    for student in unit_students:
        student_attendance_entry = student.to_dict()

        student_attendance_entry["attendances"] = []

        result.append(student_attendance_entry)
        # TODO: need to generate the attendances. Start here next time

    return OperationResult(success=True, message="Unit attendances found", data=result)


def __generate_student_exam_score_data(
    student: Student, exam: Exam, exam_score_list: list[ExamScore]
):
    exam_score_record = next(
        (record for record in exam_score_list if record.student_id == student.id), None
    )
    if exam_score_record:
        return exam_score_record
    else:
        return ExamScore.create_default(exam, student)


def get_unit_exam_scores(unit_code, exam_id):
    unit = Unit.find_by_code(unit_code)

    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    exam = Exam.find_by_id(exam_id)

    if exam is None:
        return OperationResult(success=False, message="Exam not found")

    if unit.grade.code != exam.grade.code:
        return OperationResult(
            success=False, message="Unit and exam are not in the same grade"
        )

    all_students = unit.students
    exam_score_list = ExamScore.query.filter(
        ExamScore.exam_id == exam.id,
        ExamScore.student_id.in_([student.id for student in all_students]),
    ).all()

    result_exam_score_list = []
    for student in all_students:
        exam_score_entry = __generate_student_exam_score_data(
            student, exam, exam_score_list
        )
        result_exam_score_list.append(exam_score_entry.to_dict())

    return OperationResult(
        success=True, message="Unit exam scores found", data=result_exam_score_list
    )


def update_student_exam_score_in_a_unit(unit_code, exam_id, student_code, score):
    unit = Unit.find_by_code(unit_code)

    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    exam = Exam.find_by_id(exam_id)

    if exam is None:
        return OperationResult(success=False, message="Exam not found")

    if unit.grade.code != exam.grade.code:
        return OperationResult(
            success=False, message="Unit and exam are not in the same grade"
        )

    student = Student.find_by_code(student_code)

    if student is None:
        return OperationResult(success=False, message="Student not found")

    examScore = ExamScore.find_by_student_and_exam(student, exam)

    if examScore is None:
        newExamScoreEntry = ExamScore.create_default(exam, student)
        newExamScoreEntry.score = score
        db.session.add(newExamScoreEntry)

    examScore.score = score

    db.session.flush()

    return OperationResult(success=True, message="Exam score updated")
