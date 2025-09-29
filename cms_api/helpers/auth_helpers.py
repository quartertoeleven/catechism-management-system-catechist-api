from flask_login import LoginManager

from ..models import UserAccount
from ..models.base import OperationResult

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.find_by_id(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return OperationResult(False, "Unauthorized").to_json_response(
        failed_status_code=401
    )
