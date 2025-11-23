from .student_card_cli import student_card_cli_bp


def register_blueprints(app):
    app.register_blueprint(student_card_cli_bp, cli_group="student_card")
    # app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    # app.register_blueprint(auth_bp, url_prefix=url_prefix)
    # app.register_blueprint(grade_bp, url_prefix=url_prefix)
    # app.register_blueprint(unit_bp, url_prefix=url_prefix)
    # app.register_blueprint(attendance_bp, url_prefix=url_prefix)
    # app.register_blueprint(user_profile_bp, url_prefix=url_prefix)
    # app.register_blueprint(exam_bp, url_prefix=url_prefix)
    # app.register_blueprint(student_bp, url_prefix=url_prefix)
    # # cli
    # app.register_blueprint(user_account_cli_bp, cli_group="account")
    # app.register_blueprint(data_import_cli_bp, cli_group="import")
