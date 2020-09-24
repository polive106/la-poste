from app import db


class Letter(db.Model):
    __tablename__ = "letter"

    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(256))
    status = db.Column(db.String(191))
