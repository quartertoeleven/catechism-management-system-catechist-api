from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required
from cms_api.models.base import db

from ..handlers.student import create_or_update_student_exam_score

student_bp = Blueprint("student_bp", __name__)


class StudentExamScores(MethodView):
    decorators = [login_required]

    def post(self, student_code):
        request_body = request.get_json()
        result = create_or_update_student_exam_score(
            student_code,
            request_body.get("exam_id"),
            request_body.get("score"),
        )
        if result.success:
            db.session.commit()
        return result.to_json_response()


student_bp.add_url_rule(
    "/students/<string:student_code>/exam-scores",
    view_func=StudentExamScores.as_view("student_exam_scores"),
    methods=["POST"],
)
