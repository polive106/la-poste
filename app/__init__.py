import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import config
from flask.cli import with_appcontext
import click
app = Flask(__name__)

CORS(app, origins="*", supports_credentials=True)

config_name = os.getenv("FLASK_CONFIG") or "default"
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

from . import models
from .v1 import v1 as v1_blueprint

@click.command(name="create")
@with_appcontext
def create():
    db.create_all()
    print('Database created!')


@click.command(name="seed")
@with_appcontext
def seed():
    from .models.letter import Letter
    print(Letter)
    tracking_numbers = ["1A00915820380", "4P36275770836", "1K36275770836", "4G11111111110", "RK633119313NZ", "3P11111111110", "8R11111111110", "115111111111111", "5S11111111110", "3SAAAA1111111", "6P01007508742", "6T11111111110"]
    for tracking_number in tracking_numbers:
        print(tracking_number)
        letter = Letter(tracking_number=tracking_number)
        letter.add()
    print('Database seeded')

@click.command(name="drop")
@with_appcontext
def drop():
    db.drop_all()
    print('Database dropped')

app.cli.add_command(create)
app.cli.add_command(seed)
app.cli.add_command(drop)


app.register_blueprint(v1_blueprint, url_prefix="/v1")


