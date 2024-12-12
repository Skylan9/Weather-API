from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from weather_data import get_weather_data

app = Flask(__name__)
# limiter = Limiter(get_remote_address, app=app)
@app.route('/', methods=('GET', 'POST'))

def index():
    data = None
    if request.method == "POST":
        city = request.form['cityName']
        data = get_weather_data(city)
    return render_template('index.html', data=data)
# @limiter.limit("100 per day")


# def api():
#     return "hello"

if __name__ == "__main__":
    app.run(debug=True)