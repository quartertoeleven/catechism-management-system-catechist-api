from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required

from ..handlers.qrreader import read_student_qr_code

qr_reader_bp = Blueprint("qr_reader_bp", __name__)


class QrReaderAPI(MethodView):
    decorators = [login_required]

    def post(self):
        request_body = request.get_json()
        return read_student_qr_code(request_body).to_json_response()


qr_reader_bp.add_url_rule(
    "/qrreader",
    view_func=QrReaderAPI.as_view("qr_reader_endpoint"),
    methods=["POST"]
)
