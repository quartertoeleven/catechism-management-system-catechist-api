from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required

from cms_api.models.base import db

from ..handlers.attendance import (
    handle_attendance_check,
    handle_attendance_check_using_qr,
)

attendance_bp = Blueprint("attendance_bp", __name__)


class AttendanceCheckAPI(MethodView):
    decorators = [login_required]

    def post(self, grade_schedule_id):
        request_body = request.get_json()
        result = handle_attendance_check(grade_schedule_id, request_body)
        if result.success:
            db.session.commit()
        return result.to_json_response()


class AttendanceCheckQrAPI(MethodView):
    decorators = [login_required]

    def post(self, grade_schedule_id):
        request_body = request.get_json()
        result = handle_attendance_check_using_qr(grade_schedule_id, request_body)
        if result.success:
            db.session.commit()
        return result.to_json_response()


attendance_bp.add_url_rule(
    "/attendances/<int:grade_schedule_id>/check",
    view_func=AttendanceCheckAPI.as_view("attendance_check_endpoint"),
    methods=["POST"],
)

attendance_bp.add_url_rule(
    "/attendances/<int:grade_schedule_id>/qr-check",
    view_func=AttendanceCheckQrAPI.as_view("attendance_check_qr_endpoint"),
    methods=["POST"],
)
