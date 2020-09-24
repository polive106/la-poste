import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import Model, SQLAlchemy

from app.config import config

app = Flask(__name__)

CORS(app, origins="*", supports_credentials=True)

config_name = os.getenv("FLASK_CONFIG") or "default"
app.config.from_object(config[config_name])


class LukoBaseModel(Model):
    def add(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


db = SQLAlchemy(app, model_class=LukoBaseModel)

from . import models
from .v1 import v1 as v1_blueprint

app.register_blueprint(v1_blueprint, url_prefix="/v1")
