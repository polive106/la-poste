from flask import Blueprint, request, jsonify, make_response
from flask_cors import CORS
from flask import abort
from app.models.letter import Letter, LetterSchema
from app.getStatus import async_update_status
# from utils.Okapi import okapi_letter_status

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


@v1.route('/letters', methods=['GET'])
def index():
    letters = Letter.query.all()
    letter_schema = LetterSchema(many = True) # many=True to be able to represent more than one instance when .load is called
    letters = letter_schema.dump(letters)
    return make_response(jsonify({"letters": letters}))

@v1.route('/letters/<tracking_number>/update', methods=['POST'])
def ep_update_status(tracking_number):
    letter = Letter.query.filter_by(tracking_number=tracking_number).first()
    if letter is None:
        abort(404, f"Letter not found for Tracking number: {tracking_number}")
    else:
        async_update_status(tracking_number)
    return {"message": f"Update task run accepted for letter with tracking_number {tracking_number}"}, 202

@v1.route('/letters/all/update', methods=['POST'])
def ep_update_all_status():
    letters = Letter.query.all()
    for letter in letters:
        async_update_status(letter.tracking_number)
    return {"message": "Status update launched for all letters"}, 202
