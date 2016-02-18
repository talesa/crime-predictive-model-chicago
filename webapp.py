from flask import Flask, render_template

app = Flask('crime')


@app.route('/')
def hello_world():
    return render_template('showmap.html', title="Chicago crime map")

if __name__ == '__main__':
    app.run(debug=True)