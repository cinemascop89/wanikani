from flask import Flask, render_template, request, jsonify

from generate import generate_grid
import settings

app = Flask(__name__)
app.debug = settings.DEBUG

@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/generate', methods=['POST'])
def generate():
    api_key = request.form['api_key']
    poll = request.form["poll"]

    if poll == "false":
        dimensions = (int(request.form['width']), int(request.form['height']))
        generate_grid.delay(api_key, dimensions)
    return jsonify({'status': 'generating'})


if __name__ == '__main__':
    app.run()
