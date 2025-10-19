from datetime import timedelta
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user

from ...models.user_account import UserAccount
from ...models.base import db, OperationResult


def login(login_request_dict):
    login_id = login_request_dict.get("login_id")
    password = login_request_dict.get("password")

    user_account = UserAccount.find_by_login_id(login_id)

    if user_account is None:
        return OperationResult(False, "Invalid login information")

    if not check_password_hash(user_account.password, password):
        return OperationResult(False, "Invalid login information")

    # Done check. Log user in
    login_user(user_account, remember=True, duration=timedelta(days=14))

    db.session.flush()
    db.session.commit()
    return OperationResult(True, "Login success", dict(login_id=login_id))


def logout():
    logout_user()
    return OperationResult(True, "Logout success")


def get_auth_state():
    return OperationResult(True, "User profile found", current_user.to_dict())
