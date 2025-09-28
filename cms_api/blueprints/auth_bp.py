from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required

from ..handlers.auth import login, logout

auth_bp = Blueprint('auth_bp', __name__)

class LoginAPI(MethodView):
    def post(self):
        login_body_request = request.get_json()
        result = login(login_body_request)
        return result.to_json_response()

class LogoutAPI(MethodView):
    decorators = [login_required]

    def post(self):
        result = logout()
        return result.to_json_response()

auth_bp.add_url_rule(
    '/login',
    view_func=LoginAPI.as_view('login_endpoint'),
    methods=['POST']
)

auth_bp.add_url_rule(
    '/logout',
    view_func=LogoutAPI.as_view('logout_endpoint'),
    methods=['POST']
)

