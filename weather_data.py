import json
import os
from dotenv import find_dotenv, load_dotenv
from redis_server import get_item

dotenv_path = find_dotenv()
# Load up the entries as environment variables
load_dotenv(dotenv_path)
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def get_weather_data(location, date1='', date2=''):
    # Get URL 
    url = F"{BASE_URL}{location}/{date1}/{date2}?unitGroup=metric&key={API_KEY}"

    data = json.loads(get_item(url))
    if data['address'] != location:
        print(data['address'])

        data = get_item(url =url, address =location)

    weatherdata = {}
    weatherdata.update({"city" :data["address"]})
    for i in data["days"]:
        weatherdata.update({i["datetime"]: 
                    [{"tempmax": i["tempmax"]},
                    {"tempmin": i["tempmin"]},
                    {"temp": i["temp"]}]
                    }
                    )

    with open('url.json', 'w') as outfile:
        json.dump(url, outfile)
    return weatherdata
