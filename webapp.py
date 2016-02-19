from flask import Flask, render_template

app = Flask('crime')

maps = [{'name': 'Historic data', 'url': 'past.html'}, {'name': 'Prediction on tomorrow\'s weather', 'url': 'tomorrow.html'}]

@app.route('/')
@app.route('/past.html')
def past_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="past.html")

@app.route('/tomorrow.html')
def tomorrow_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="tomorrow.html")

if __name__ == '__main__':
    app.run(debug=True)