from flask import Blueprint, request
from flask.views import MethodView

from ..handlers.attendance import handle_attendance_check

attendance_bp = Blueprint("attendance_bp", __name__)


class AttendanceCheckAPI(MethodView):
    def post(self, grade_schedule_id):
        request_body = request.get_json()
        result = handle_attendance_check(grade_schedule_id, request_body)
        return result.to_json_response()


attendance_bp.add_url_rule(
    "/attendances/<int:grade_schedule_id>/check",
    view_func=AttendanceCheckAPI.as_view("attendance_check_endpoint"),
    methods=["POST"],
)
