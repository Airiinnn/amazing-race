import click
from flask.cli import with_appcontext

from app import db, Bonusstage, Mainstage, Player, Progress, Stage0, Stage1, Stage2, Stage3, Stage7

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()