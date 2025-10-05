from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required, current_user

from ..handlers.unit import get_unit_details, get_unit_list_for_a_catechist, get_unit_attendances_for_schedule

unit_bp = Blueprint("unit_bp", __name__)


class UnitsAPI(MethodView):
    decorators = [login_required]

    def get(self):
        study_year = request.args.get("study_year")
        result = get_unit_list_for_a_catechist(current_user.catechist, study_year)
        return result.to_json_response()


class UnitAPI(MethodView):
    def get(self, unit_code):
        unit_details = get_unit_details(unit_code, include_students=True)
        return unit_details.to_json_response()
    
class UnitScheduleAPI(MethodView):
    def get(self, unit_code):
        schedule_id = request.args.get("schedule_id")
        type = request.args.get("type")
        result = get_unit_attendances_for_schedule(unit_code, schedule_id, type)
        return result.to_json_response()


unit_bp.add_url_rule(
    "/units", view_func=UnitsAPI.as_view("units_api_endpoint"), methods=["GET"]
)

unit_bp.add_url_rule(
    "/units/<string:unit_code>",
    view_func=UnitAPI.as_view("unit_api_endpoint"),
    methods=["GET"],
)

unit_bp.add_url_rule(
    "/units/<string:unit_code>/schedules",
    view_func=UnitScheduleAPI.as_view("unit_schedule_api_endpoint"),
    methods=["GET"],
)