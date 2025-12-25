import click
from flask import Blueprint

from cms_api.models.base import db
from ...handlers.data_import import import_unit_students_from_excel

data_import_cli_bp = Blueprint("data_import_cli_bp", __name__)


@data_import_cli_bp.cli.command("unitstudents")
@click.argument("file_path")
def import_students(file_path):
    excel_file = open(file_path, "rb")
    result = import_unit_students_from_excel(excel_file)
    if result.success:
        db.session.commit()
        click.echo(result.message)
        click.echo(result.data)
    else:
        click.echo(result.message, err=True)


# import click

# from flask import Blueprint

# from ...handlers.user_account import create_user_account, reset_account_password
# from ...models.base import db

# user_account_cli_bp = Blueprint("user_account_cli_bp", __name__)


# @user_account_cli_bp.cli.command("create")
# @click.argument("login_id")
# @click.argument("password", required=False)
# def create(login_id, password=None):
#     result = create_user_account(login_id, password)
#     if result.success:
#         db.session.commit()
#         click.echo(result.message)
#         click.echo(result.data)
#     else:
#         click.echo(result.message, err=True)


# @user_account_cli_bp.cli.command("resetpwd")
# @click.argument("login_id")
# def reset_password(login_id):
#     result = reset_account_password(login_id)
#     if result.success:
#         db.session.commit()
#         click.echo(result.message)
#         click.echo(result.data)
#     else:
#         click.echo(result.message, err=True)
