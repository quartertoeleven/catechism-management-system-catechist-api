from flask import Blueprint, request
from flask.views import MethodView

from ..handlers.unit import get_unit_details

unit_bp = Blueprint('unit_bp', __name__)

class UnitAPI(MethodView):
    def get(self, unit_code):
        unit_details = get_unit_details(unit_code, include_students=True)
        return unit_details.to_json_response()
    
unit_bp.add_url_rule(
    '/units/<string:unit_code>',
    view_func=UnitAPI.as_view('unit_api_endpoint'),
    methods=['GET']
)
