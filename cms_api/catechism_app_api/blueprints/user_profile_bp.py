from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required

from ...models.base import db
from ..handlers.user_account import change_account_password

user_profile_bp = Blueprint("user_profile_bp", __name__)


class ChangePasswordAPI(MethodView):
    decorators = [login_required]

    def post(self):
        request_body = request.get_json()
        result = change_account_password(
            request_body.get("current_password") or "",
            request_body.get("new_password") or "",
            request_body.get("confirm_password"),
        )
        if result.success:
            db.session.commit()
        return result.to_json_response()


user_profile_bp.add_url_rule(
    "/account/change-password",
    view_func=ChangePasswordAPI.as_view("change_password_endpoint"),
    methods=["POST"],
)
