from flask import Blueprint, jsonify
from flask.views import MethodView

user_account_bp = Blueprint('user_account_bp', __name__)

class UserAccountsAPI(MethodView):
    def post(self):

        
        return jsonify(
            success=True,
            message="Server is up and running"
        )
    
user_account_endpoint = UserAccountsAPI.as_view('user_account_endpoint')
user_account_bp.add_url_rule(
    '/accounts',
    view_func=user_account_endpoint,
    methods=['GET']
)