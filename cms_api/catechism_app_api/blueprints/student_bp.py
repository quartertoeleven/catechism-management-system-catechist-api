from flask import Blueprint, request
from flask.views import MethodView
from flask_login import login_required
from cms_api.models.base import db

from ..handlers.student import (
    create_or_update_student_exam_score,
    get_student_details,
    update_student_details,
    create_or_update_student_contacts,
    delete_student_contact,
    update_student_year_end_result
)

student_bp = Blueprint("student_bp", __name__)


class StudentDetailsAPI(MethodView):
    decorators = [login_required]

    def get(self, student_code):
        return get_student_details(student_code).to_json_response()

    def put(self, student_code):
        request_body = request.get_json()
        result = update_student_details(student_code, request_body)
        if result.success:
            db.session.commit()
        return result.to_json_response()

class StudentContactsAPI(MethodView):
    decorators = [login_required]
    
    def post(self, student_code):
        request_body = request.get_json()
        result = create_or_update_student_contacts(student_code, request_body)
        if result.success:
            db.session.commit()
        return result.to_json_response()
    
    def delete(self, student_code, contact_id):
        result = delete_student_contact(student_code, contact_id)
        if result.success:
            db.session.commit()
        return result.to_json_response()


class StudentExamScoresAPI(MethodView):
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

class StudentYearEndResultsAPI(MethodView):
    decorators = [login_required]
    
    def post(self, student_code):
        request_body = request.get_json()
        result = update_student_year_end_result(student_code, request_body)
        if result.success:
            db.session.commit()
        return result.to_json_response()


student_bp.add_url_rule(
    "/students/<string:student_code>",
    view_func=StudentDetailsAPI.as_view("student_details"),
    methods=["GET", "PUT"],
)

student_bp.add_url_rule(
    "/students/<string:student_code>/exam-scores",
    view_func=StudentExamScoresAPI.as_view("student_exam_scores"),
    methods=["POST"],
)

student_bp.add_url_rule(
    "/students/<string:student_code>/contacts",
    view_func=StudentContactsAPI.as_view("student_contacts"),
    methods=["POST"]
)

student_bp.add_url_rule(
    "/students/<string:student_code>/contacts/<int:contact_id>",
    view_func=StudentContactsAPI.as_view("student_contacts_removal"),
    methods=["DELETE"]
)

student_bp.add_url_rule(
    "/students/<string:student_code>/year-end-results",
    view_func=StudentYearEndResultsAPI.as_view("student_year_end_results"),
    methods=["POST"]
)
