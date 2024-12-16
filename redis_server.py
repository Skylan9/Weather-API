from fastapi import FastAPI
from redis import Redis
import httpx
import json
import requests
from json.decoder import JSONDecodeError

app = FastAPI()
redis_client = Redis(host='localhost', port=6379, db=1)

@app.on_event("startup")
async def startup_even():
    app.state.redis = Redis(host='localhost', port = 6379)
    app.state.http_client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.redis.close()

@app.get('/weather_data')
async def read_item():

    value = app.state.redis.get('weather_data')

    if value is None:
        url = get_url()
        response = await app.state.http_client.get(url)
        value = response.json()
        app.state.redis.set('weather_data', json.dumps(value))
        app.state.redis.expire('weather_data', 40000)
    print(value)
    return json.loads(value)

# URL that has been last searched by the user per city
def get_url():
    with open('url.json') as urlfile:
        url = json.load(urlfile)
    return url
# Get data from cache or API
def get_item(url, address=''):
    # Attempt to parse the JSON string from the Redis server
    value = redis_client.get('weather_data')
    
    if value is None or address != '':
        # Attempt to parse the JSON string
        response =  requests.get(url)
        value = response.json()
        redis_client.set('weather_data', json.dumps(value))
        redis_client.expire('weather_data', 40000)
    return value
        
    