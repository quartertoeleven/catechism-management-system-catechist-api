from .health_check_bp import health_check_bp
from .auth_bp import auth_bp

from .grade_bp import grade_bp
from .unit_bp import unit_bp
from .attendance_bp import attendance_bp
from .user_profile_bp import user_profile_bp

from .exam_bp import exam_bp


from .cli.user_account_cli import user_account_cli_bp
from .cli.data_import_cli import data_import_cli_bp


def register_blueprints(app, url_prefix):
    app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    app.register_blueprint(auth_bp, url_prefix=url_prefix)
    app.register_blueprint(grade_bp, url_prefix=url_prefix)
    app.register_blueprint(unit_bp, url_prefix=url_prefix)
    app.register_blueprint(attendance_bp, url_prefix=url_prefix)
    app.register_blueprint(user_profile_bp, url_prefix=url_prefix)
    app.register_blueprint(exam_bp, url_prefix=url_prefix)
    # cli
    app.register_blueprint(user_account_cli_bp, cli_group="account")
    app.register_blueprint(data_import_cli_bp, cli_group="import")
