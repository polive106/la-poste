from app import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy

class Letter(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(191), nullable=True)
    tracking_number = db.Column(db.String(256))

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, tracking_number, status = None):
        self.tracking_number = tracking_number
        self.status = status
    def __repr__(self):
        return '<Letter %d>' % self.id

# NOW WE USE MARSHMALLOW TO DEFINE THE OUTPUT SCHEMA OF LETTER
class LetterSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Letter
        sqla_session = db.session

    id = fields.Integer(dump_only = True)
    status = fields.String(required = False)
    tracking_number = fields.String(required = True)
