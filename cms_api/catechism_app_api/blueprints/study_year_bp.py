from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required
from cms_api.models.base import db

from ..handlers.study_year import get_study_year_general_schedules

study_year_bp = Blueprint("study_year_bp", __name__)


class StudyYearSchedules(MethodView):
    decorators = [login_required]

    def get(self, study_year_code):
        result = get_study_year_general_schedules(study_year_code)
        return result.to_json_response()


study_year_bp.add_url_rule(
    "/study_years/<string:study_year_code>/schedules",
    view_func=StudyYearSchedules.as_view("study_year_schedule_endpoint"),
    methods=["GET"],
)
