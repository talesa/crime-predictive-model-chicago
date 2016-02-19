from flask import Flask, render_template


app = Flask('crime')

maps = [{'name': 'past', 'url': 'past.html'}, {'name': 'battery', 'url': 'battery.html'}]

@app.route('/')
@app.route('/past.html')
def past_data():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="past.html")

@app.route('/battery.html')
def battery():
    return render_template('showmap.html', title="Chicago crime map", maps=maps, current="battery.html")

if __name__ == '__main__':
    app.run(debug=True)