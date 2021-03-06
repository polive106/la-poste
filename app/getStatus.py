from . import celery
import redis
import os
from dotenv import load_dotenv
from app.config import config, Config
from app.models.letter import Letter
from urllib.parse import urlparse
import requests
import json

# Set Redis connection:
config_name = os.getenv("FLASK_CONFIG") or "default"
redis_url = urlparse(config[config_name].CELERY_BROKER_URL)
r = redis.StrictRedis(host=redis_url.hostname, port=redis_url.port, db=1, password=redis_url.password)

# Test the Redis connection:
try:
    r.ping()
    print("Redis is connected!")
except redis.ConnectionError:
    print("Redis connection error!")



@celery.task()
def update_status(tracking_number):
    # Load .env content
    load_dotenv()
    # select letter to be updated in db
    letter = Letter.query.filter_by(tracking_number=tracking_number).first()
    # sending get request and saving response as response object
    API_ENDPOINT = f'https://api.laposte.fr/suivi/v2/idships/{tracking_number}?lang=fr_FR'
    API_KEY = os.getenv('API_KEY')
    headers = {'X-Okapi-Key': API_KEY, 'Accept':'application/json', 'Content-Type': 'application/json'}
    r = requests.get(url = API_ENDPOINT, headers = headers)
    # Try / except here --> Okapi JSON are faulty (missing ',' in JSON ) in sandbox env
    try:
        json_data = json.loads(r.text)
        new_status = json_data['shipment']['timeline'][-1]['shortLabel']
        letter.status = new_status
        letter.add()
    except:
        new_status = "Statut indisponible"
        letter.status = new_status
        letter.add()

def async_update_status(tracking_number):
    update_status.delay(tracking_number)
    return




