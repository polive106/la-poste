import os
import requests
import json
from flask import current_app
@current_app.celery.task
def get_last(code):
    # defining the api-endpoint
    API_ENDPOINT = f'https://api.laposte.fr/suivi/v2/idships/{code}?lang=fr_FR'
    # data to be sent to api
    API_KEY = os.getenv('API_KEY')
    headers = {'X-Okapi-Key': API_KEY, 'Accept':'application/json', 'Content-Type': 'application/json'}
    # sending get request and saving response as response object
    r = requests.get(url = API_ENDPOINT, headers = headers)
    # get data as json
    try:
        json_data = json.loads(r.text)
        return json_data['shipment']['timeline'][-1]['shortLabel']
    except:
        return "Statut indisponible"
