import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.cli import with_appcontext
from app.config import config
import click
from celery import Celery

config_name = os.getenv("FLASK_CONFIG") or "default"
celery = Celery(__name__, broker=config[config_name].CELERY_BROKER_URL)
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    config_name = os.getenv("FLASK_CONFIG") or "default"
    CORS(app, origins="*", supports_credentials=True)
    app.config.from_object(config[config_name])
    celery.conf.update(app.config)
    db.init_app(app)

    with app.app_context(): # app_context needed to import blueprints / letters => mostly for celery
        from .models.letter import Letter
        from .v1 import v1 as v1_blueprint
        app.register_blueprint(v1_blueprint, url_prefix="/v1")


    # CLI cmd to create DB
    @click.command(name="db_create")
    @with_appcontext
    def create():
        db.create_all()
        print('Database created!')

    # CLI cmd to seed DB with sandbox env examples from OKAPI
    @click.command(name="db_seed")
    @with_appcontext
    def seed():
        from .models.letter import Letter
        print(Letter)
        tracking_numbers = ["1A00915820380", "4P36275770836", "1K36275770836", "4G11111111110", "RK633119313NZ", "3P11111111110", "8R11111111110", "115111111111111", "5S11111111110", "3SAAAA1111111", "6P01007508742", "6T11111111110", "6W111111111XX", "FD633119313NZ", "GF111111110NZ", "114111111111111", "GM111111110NZ", "ZZ111111110NZ", "FA633119313XX", "6C12345678910", "6C22345678999"]
        for tracking_number in tracking_numbers:
            print(tracking_number)
            letter = Letter(tracking_number=tracking_number)
            letter.add()
        print('Database seeded')

    # CLI cmd to drop DB
    @click.command(name="db_drop")
    @with_appcontext
    def drop():
        db.drop_all()
        print('Database dropped')

    # Create CLI cmd after definition
    app.cli.add_command(create)
    app.cli.add_command(seed)
    app.cli.add_command(drop)



    return app

if __name__ == "__main__":
    app.run(host='0.0.0.0')
