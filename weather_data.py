import requests
import json
import os
from dotenv import find_dotenv, load_dotenv
import redis
from dataclasses import dataclass

# Connect to the redis database
redis_client = redis.Redis(host='localhost', port=6379, db=0)
# Find .env file in one of the directories of the project
dotenv_path = find_dotenv()
# Load up the entries as environment variables
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

@dataclass
class WeatherData:
    city: str
    temperature: float

def get_weather_data(location, date1='', date2=''):
    url = F"{BASE_URL}{location}/{date1}/{date2}?unitGroup=metric&key={API_KEY}"
    data = redis_client.get('weather_data')
    data = json.loads(data)
    if data is None or data["address"] != location:
        print("Could not find data in cache, retrieving from API")
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            redis_client.set('weather_data', json.dumps(data))
            redis_client.expire('weather_data', 86400)
    else:
       
        print("Found data in cache")
    
    weatherData = WeatherData(
        city= data["address"],
        temperature= data["days"][0]["temp"]
    )
    return weatherData
