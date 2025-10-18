from datetime import datetime
from pandas import read_excel, isna, NA, ExcelFile

from ..models import Unit, Student, UnitStudent
from ..models.base import OperationResult, db

from ..helpers.enums import GenderEnum

def __get_middle_name(first_name_from_excel):
    return ' '.join(first_name_from_excel.split(' ')[1:]) if first_name_from_excel else None

def __get_gender(gender_from_excel):
    return GenderEnum.MALE if gender_from_excel == "Nam" else GenderEnum.FEMALE

def __get_date_of_birth(date_of_birth_from_excel):
    return datetime.strptime(date_of_birth_from_excel, "%d/%m/%Y").date() if date_of_birth_from_excel else None

def import_unit_students_from_excel(excel_file):
    xl = ExcelFile(excel_file)
    wb = xl.book
    sh = wb["Sheet1"]
    student_df = read_excel(
        excel_file,
        sheet_name="Sheet1",
        header=4,
        dtype="string"
    )
    unit_code = sh["B3"].value

    unit = Unit.find_by_code(unit_code)
    if unit is None:
        return OperationResult(success=False, message="Unit not found")

    student_df.replace({NA: None})
    student_dict_from_excel = student_df.to_dict(orient="records")
    student_list = []
    for student_dict in student_dict_from_excel:
        print(student_dict)
        new_student = Student(
            code=student_dict["Mã học viên"],
            saint_name=student_dict["Tên Thánh"],
            last_name=student_dict["Họ"].split(' ')[0],
            middle_name=__get_middle_name(student_dict["Họ"]),
            first_name=student_dict["Tên"],
            gender=__get_gender(student_dict["Giới tính"]),
            date_of_birth=__get_date_of_birth(student_dict.get("Ngày Sinh").strip()) if student_dict.get("Ngày Sinh") else None,
        )
        student_list.append(new_student)
    
    db.session.add_all(student_list)
    db.session.flush()

    for student in student_list:
        new_unit_student = UnitStudent(
            student_id=student.id,
            unit_id=unit.id,
        )
        db.session.add(new_unit_student)

    db.session.flush()

    return OperationResult(success=True, message="Import successfully")
