from flask import Blueprint
from flask_cors import CORS

from app.models.letter import Letter

v1 = Blueprint("v1", __name__)
CORS(v1)


@v1.route('/ping', methods=['GET'])
def ep_ping():
    return "pong", 200


@v1.route('/create_letter', methods=['POST'])
def ep_setup_create_letter():
    # Example of ORM usage (SQLAlchemy)
    letter = Letter()
    letter.add()
    return f"All done : letter object {letter.id} has been created", 200
