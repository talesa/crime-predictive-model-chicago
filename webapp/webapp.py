from flask import Flask, render_template

import requests

r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Chicago&mode=json&units=metric&cnt=7&appid=44db6a862fba0b067b1930da0d769e98')
r.headers
data = r.json()["list"][1]
weather_tomorrow = {'temp': data['temp']['max'], 'rain': 0}
if('rain' in data.keys()):
        weather_tomorrow['rain'] = data['rain']['3h']*10

#TODO: save map as tomorrow.html

app = Flask('crime')

maps = [{'name': 'Historic data', 'url': 'past.html'}, {'name': 'Prediction on tomorrow\'s weather', 'url': 'tomorrow.html'}]

@app.route('/')
@app.route('/past.html')
def past_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="past.html")

@app.route('/tomorrow.html')
def battery():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="tomorrow.html")

if __name__ == '__main__':
    app.run(debug=True)