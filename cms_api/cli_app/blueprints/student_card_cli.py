import click
from flask import Blueprint

from ..handlers.student_card import generate_student_card, generate_unit_student_cards

student_card_cli_bp = Blueprint("student_card_cli_bp", __name__)


@student_card_cli_bp.cli.command("create")
@click.argument("type")
@click.argument("code")
@click.argument("dest_path")
def create_student_card(type, code, dest_path):
    match type:
        case "student":
            result = generate_student_card(code, dest_path)
            click.echo(result.message)
        case "unit":
            result = generate_unit_student_cards(code, dest_path)
            click.echo(result.message)
        case _:
            raise Exception("Invalid type")
