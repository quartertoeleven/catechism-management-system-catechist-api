from .health_check_bp import health_check_bp

from .cli.user_account_cli import user_account_cli_bp

def register_blueprints(app, url_prefix):
    app.register_blueprint(health_check_bp, url_prefix=url_prefix)
    # cli
    app.register_blueprint(user_account_cli_bp, cli_group="account")
