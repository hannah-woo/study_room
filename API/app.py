from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/map')
def show_map():
    return render_template('map.html')

@app.route('/maps')
def show_maps():
    return render_template('maps.html')


app.run(host='localhost', port=8080, debug=True)