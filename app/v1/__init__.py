from flask import Blueprint, request
from flask_cors import CORS
from flask import abort
from app.models.letter import Letter

v1 = Blueprint("v1", __name__)
CORS(v1)





@v1.route('/ping', methods=['GET'])
def ep_ping():
    return "pong", 200


@v1.route('/letters', methods=['POST'])
def ep_setup_create_letter():
    # Example of ORM usage (SQLAlchemy)
    body_data = request.get_json()
    if body_data.get("tracking_number"):
        status = body_data["status"] if body_data.get("status") else None
        tracking_number= body_data["tracking_number"]
        print(body_data)
        letter = Letter(tracking_number=tracking_number, status=status)
        letter.add()
        return f"All done : letter object {letter.id} has been created", 200
    else:
        abort(400, 'Please specify at least a tracking number')
