import hashlib

from flask import Flask, render_template, request, jsonify
from boto.s3.connection import S3Connection
from boto.s3.bucket import Bucket

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
    else:
        image_path = "images/{0}.png".format(hashlib.md5(api_key).hexdigest())
        conn = S3Connection(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)
        bucket = Bucket(conn, settings.S3_BUCKET)
        if bucket.get_key(image_path):
            return jsonify({'status': 'ok', 'path': image_path})
        else:
            return jsonify({'status': 'generating'})


if __name__ == '__main__':
    app.run()
