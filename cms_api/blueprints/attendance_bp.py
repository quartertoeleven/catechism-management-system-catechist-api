from flask import Blueprint, jsonify
from flask.views import MethodView

attendance_bp = Blueprint('attendance_bp', __name__)

class AttendanceCheckAPI(MethodView):
    def post(self):
        pass
    
# health_check_endpoint = HealthCheckAPI.as_view('health_check_endpoint')
# attendance_bp.add_url_rule(
#     '/health-check',
#     view_func=health_check_endpoint,
#     methods=['GET']
# )