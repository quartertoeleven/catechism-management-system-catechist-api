import re, string, random

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user

from ...helpers.constants import VALID_EMAIL_REGEX

from ...models import UserAccount, StudyYear
from ...models.base import db, OperationResult


def __generate_strong_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(length))
    if (
        any(c.isupper() for c in password)
        and any(c.islower() for c in password)
        and any(c.isdigit() for c in password)
        and any(c in string.punctuation for c in password)
    ):
        return password
    return __generate_strong_password(length)


def create_user_account(login_id, password=None) -> OperationResult:
    if re.match(VALID_EMAIL_REGEX, login_id) is None:
        return OperationResult(False, "Login ID must be a valid email address")

    if password is not None:
        password_len = len(password)
        if password_len < 8 or password_len > 32:
            return OperationResult(
                False, "Password must be between 8 and 32 characters"
            )

    if UserAccount.find_by_login_id(login_id) is not None:
        return OperationResult(False, "Login ID already exists")

    password = password or __generate_strong_password()

    hashed_password = generate_password_hash(password)

    user_account = UserAccount(login_id=login_id, password=hashed_password)

    db.session.add(user_account)
    db.session.flush()

    return OperationResult(
        True,
        "User account {login_id} created".format(login_id=login_id),
        dict(login_id=login_id, password=password),
    )


def reset_account_password(login_id):
    user_account = UserAccount.find_by_login_id(login_id)
    if user_account is None:
        return OperationResult(False, "User account not found")

    new_password = __generate_strong_password()
    user_account.password = generate_password_hash(new_password)

    db.session.flush()

    return OperationResult(
        True,
        "Password reset successfully for {login_id}".format(login_id=login_id),
        dict(password=new_password),
    )


def get_current_user_profile():
    result = current_user.to_dict()

    current_unit_dict = None
    current_grade_dict = None

    if current_user.catechist is not None:
        current_catechist = current_user.catechist
        current_study_year = StudyYear.get_current()
        all_catechist_units = current_catechist.units

        if len(all_catechist_units) > 0:
            current_unit = list(
                filter(
                    lambda unit: unit.grade.study_year_id == current_study_year.id,
                    all_catechist_units,
                )
            )

        current_unit_dict = current_unit[0].to_dict() if len(current_unit) > 0 else None
        current_grade_dict = current_unit[0].grade.to_dict()

    result["current_unit"] = current_unit_dict
    result["current_grade"] = current_grade_dict

    return OperationResult(True, "User profile found", result)


def change_account_password(
    current_password: string, new_password: string, confirm_password: string
) -> OperationResult:

    if len(new_password) < 8:
        return OperationResult(False, "Mật khẩu phải chứa ít nhất 8 kí tự")

    if len(new_password) > 32:
        return OperationResult(False, "Mật khẩu dài tối đa 32 kí tự")

    if new_password != confirm_password:
        return OperationResult(False, "Xác nhận mật khẩu không khớp")

    if not check_password_hash(current_user.password, current_password):
        return OperationResult(False, "Mật khẩu hiện tại không đúng")

    current_user.password = generate_password_hash(new_password)

    db.session.flush()

    return OperationResult(
        True,
        "Thay đổi mật khẩu thành công",
    )
