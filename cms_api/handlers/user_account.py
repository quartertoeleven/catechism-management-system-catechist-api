import re, string, random

from werkzeug.security import generate_password_hash

from ..helpers.constants import VALID_EMAIL_REGEX

from ..models import UserAccount
from ..models.base import db, OperationResult


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
