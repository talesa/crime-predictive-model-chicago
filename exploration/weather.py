import requests

def fetch():
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q=Chicago&mode=json&units=metric&cnt=7&appid=44db6a862fba0b067b1930da0d769e98')
    #import ipdb; ipdb.set_trace()
    data = r.json()["list"][1]
    weather_tomorrow = {'temp': data['temp']['max'], 'rain': 0}
    if('rain' in data.keys()):
            weather_tomorrow['rain'] = data['rain']['3h']*10
    return weather_tomorrow
