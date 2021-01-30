from . import celery
import redis
import os
from app.config import config, Config
from urllib.parse import urlparse
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


@celery.task(name='tasks.async_run_get_manifest')
def get_status(tracking_number):
    # defining the api-endpoint
    API_ENDPOINT = f'https://api.laposte.fr/suivi/v2/idships/{tracking_number}?lang=fr_FR'
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


def async_get_status(tracking_number):
    get_status(tracking_number)
    return
