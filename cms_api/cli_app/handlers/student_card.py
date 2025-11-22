import segno, imgkit, base64, os

from flask import render_template

from cms_api.helpers.enums import GenderEnum
from cms_api.models import Student, Unit
from cms_api.models.base import OperationResult


def __render_student_card_front(student: Student):
    qr_str = "{}|{}".format(
        "CMS_V1",
        base64.b64encode(bytes(student.v1_qr_code_str, "utf-8")).decode("utf-8"),
    )
    qr_code = segno.make(qr_str, version=10, error="Q")

    student_card_front_html = render_template(
        "student_card/front.html",
        saint_name=student.saint_name,
        full_name=student.full_name,
        dob=(
            student.date_of_birth.strftime("%d/%m/%Y")
            if student.date_of_birth
            else ("chưa cập nhật")
        ),
        student_code=student.code,
        gender="Nam" if student.gender == GenderEnum.MALE else "Nữ",
        qr_svg=qr_code.svg_inline(scale=4.8, dark="505050"),
    )

    return student_card_front_html


def __render_student_card_back():
    student_card_back_html = render_template("student_card/back.html")
    return student_card_back_html


def generate_student_card(code, dest_path) -> OperationResult:
    png_config = {"crop-h": "650", "crop-w": "1004", "quality": 89}
    existing_student = Student.find_by_code(code)

    if existing_student is None:
        print("Student with code {} is not found".format(code))
        return OperationResult(False, "Failed to create student card")

    front_html = __render_student_card_front(existing_student)
    back_html = __render_student_card_back()

    imgkit.from_string(
        front_html,
        f"{dest_path}/{existing_student.code}-side1.png",
        options=png_config,
    )

    imgkit.from_string(
        back_html,
        f"{dest_path}/{existing_student.code}-side2.png",
        options=png_config,
    )

    return OperationResult(True, "Student card created")


def generate_unit_student_cards(code, dest_path) -> OperationResult:
    existing_unit = Unit.find_by_code(code)

    if existing_unit is None:
        print("Unit with code {} is not found".format(code))
        return OperationResult(False, "Failed to create student card")

    if not os.path.exists(f"{dest_path}/{existing_unit.code}"):
        os.makedirs(f"{dest_path}/{existing_unit.code}")

    for student in existing_unit.students:

        print("Generating student card for {}".format(student.code))
        print("Raw data for {}".format(student.to_dict()))

        front_html = __render_student_card_front(student)
        back_html = __render_student_card_back()

        imgkit.from_string(
            front_html,
            f"{dest_path}/{existing_unit.code}/{student.code}-side1.png",
            options={"crop-h": "650", "crop-w": "1004", "quality": 89},
        )

        imgkit.from_string(
            back_html,
            f"{dest_path}/{existing_unit.code}/{student.code}-side2.png",
            options={"crop-h": "650", "crop-w": "1004", "quality": 89},
        )

    return OperationResult(True, "Student card created")
