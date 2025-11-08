from flask import Blueprint
from flask_login import login_required
from flask.views import MethodView

from ...models.base import db

from ..handlers.grade import get_grade_schedules, get_grade_units, get_grade_exams

grade_bp = Blueprint("grade_bp", __name__)


class GradeSchedulesAPI(MethodView):
    decorators = [login_required]

    def get(self, grade_code):
        result = get_grade_schedules(grade_code)
        return result.to_json_response()


class GradeUnitsAPI(MethodView):
    decorators = [login_required]

    def get(self, grade_code):
        result = get_grade_units(grade_code)
        return result.to_json_response()


class GradeExamsAPI(MethodView):
    decorators = [login_required]

    def get(self, grade_code):
        result = get_grade_exams(grade_code)
        return result.to_json_response()


grade_bp.add_url_rule(
    "/grades/<string:grade_code>/schedules",
    view_func=GradeSchedulesAPI.as_view("grade_schedules_endpoint"),
    methods=["GET"],
)

grade_bp.add_url_rule(
    "/grades/<string:grade_code>/exams",
    view_func=GradeExamsAPI.as_view("grade_exams_endpoint"),
    methods=["GET"],
)
