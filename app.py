from StringIO import StringIO

from flask import Flask, render_template, request, make_response

from api import Wanikani
from generate import generate_grid

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/generate', methods=['POST'])
def generate():
    api_key = request.form['api_key']
    client = Wanikani(api_key)
    user_progress = client.kanji()
    dimensions = (int(request.form['width']), int(request.form['height']))

    image = generate_grid(user_progress['requested_information'], dimensions)
    image_io = StringIO()
    image.save(image_io, 'PNG')
    response = make_response(image_io.getvalue())
    response.content_type = 'image/png'

    return response

if __name__ == '__main__':
    app.run()
