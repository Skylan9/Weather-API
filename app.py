from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from weather_data import get_weather_data
from flask_table import Table, Col
import subprocess

app = Flask(__name__)

#Code to run before initialization off the Flask application
@app.before_first_request
def run_once():
    # Connect to the redis database
    subprocess.Popen(["python", "start_redis.py"])

@app.route('/', methods=('GET', 'POST'))

def index():
    data = None
    today = None
    temp = None
    tempmin = None
    tempmax = None
    city = None

    if request.method == "POST":
        try:
            city = request.form['cityName']
            data = get_weather_data(city)
            # print(data)
            
            # (k := next(iter(d)), d.pop(k))
            city = data[list(data.keys())[0]]
            data.pop(next(iter(data)))
            print(data.get(next(iter(data)))[2].get("temp"))
            
            today = data.get(next(iter(data)))
            temp = data.get(next(iter(data)))[2].get("temp")
            tempmin = data.get(next(iter(data)))[1].get("tempmin")
            tempmax = data.get(next(iter(data)))[0].get("tempmax")
        except:
            error_message = "This city does not exists or is not in the database"
            return render_template('index.html', error_message=error_message)
        else:
            return render_template('index.html', data=data, city=city, today=today, temp=temp, tempmin=tempmin, tempmax=tempmax)
# @limiter.limit("100 per day")


# def api():
#     return "hello"

if __name__ == "__main__":
    app.run(debug=True)