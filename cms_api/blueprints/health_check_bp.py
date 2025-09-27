from flask import Blueprint, jsonify
from flask.views import MethodView

health_check_bp = Blueprint('health_check_bp', __name__)

class HealthCheckAPI(MethodView):
    def get(self):
        return jsonify(
            success=True,
            message="Server is up and running"
        )
    
health_check_endpoint = HealthCheckAPI.as_view('health_check_endpoint')
health_check_bp.add_url_rule(
    '/health-check',
    view_func=health_check_endpoint,
    methods=['GET']
)