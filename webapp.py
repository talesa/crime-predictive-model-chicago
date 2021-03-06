from flask import Flask, render_template
import exploration.weather as weather
#import exploration.adam_prediction_bins 
#this would load the new weather data and update tomorrow's map, but the file needs to be exported from its notebook

tomorrow_weather = weather.fetch()
app = Flask('crime')

maps = [{'name': 'Historic data', 'url': 'past.html'}, {'name': 'Prediction on tomorrow\'s weather', 'url': 'tomorrow.html'}]

@app.route('/')
@app.route('/past.html')
def past_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="past.html")

@app.route('/tomorrow.html')
def tomorrow_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="tomorrow.html", weather=tomorrow_weather)

if __name__ == '__main__':
    app.run(debug=True)
