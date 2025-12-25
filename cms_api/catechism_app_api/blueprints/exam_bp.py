from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required

from cms_api.models.base import db

from ..handlers.exam import create_or_update_exam, remove_exam

exam_bp = Blueprint("exam_bp", __name__)


class ExamsAPI(MethodView):
    decorators = [login_required]

    def post(self):
        request_body = request.get_json()
        result = create_or_update_exam(request_body)
        if result.success:
            db.session.commit()

        return result.to_json_response()


class ExamAPI(MethodView):
    decorators = [login_required]

    def delete(self, exam_id):
        result = remove_exam(exam_id)

        if result.success:
            db.session.commit()
        return result.to_json_response()


exam_bp.add_url_rule(
    "/exams", view_func=ExamsAPI.as_view("exams_endpoint"), methods=["POST"]
)
exam_bp.add_url_rule(
    "/exams/<int:exam_id>",
    view_func=ExamAPI.as_view("exam_endpoint"),
    methods=["DELETE"],
)
