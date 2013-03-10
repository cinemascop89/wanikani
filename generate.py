# -*- coding: utf-8 -*-
import math
import hashlib
from cStringIO import StringIO

from PIL import Image, ImageFont, ImageDraw
from celery import Celery
from boto.s3.bucket import Bucket
from boto.s3.connection import S3Connection
from boto.s3.key import Key

import grid
import settings
from api import Wanikani

celery = Celery('tasks', broker=settings.CELERY_BROKER_URL)


def generate_user_table(user_progress):

    table = {}
    for kanji in user_progress:
        stats = kanji['stats']
        if stats:
            table[kanji['character']] = stats['srs']

    return table


@celery.task(ignore_result=True)
def generate_grid(api_key, dimensions):

    client = Wanikani(api_key)
    user_progress = client.kanji()['requested_information']
    print "User information received"

    colors = {
        'apprentice':0xDD0093,
        'guru': 0x882D9E,
        'master': 0x94DDB,
        'enlighten': 0x0093DD,
        'burned': 0x434343,
        'locked': 0x101010,
    }

    user_table = generate_user_table(user_progress)
    image_width, image_height = dimensions
    font_size = int(math.sqrt(image_width * image_height / len(grid.kanji)))

    image = Image.new("RGB", dimensions)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ipag.ttf", font_size, encoding='utf-8')

    x, y = 0, 0
    for i, kanji in enumerate(grid.kanji):
        color = colors[user_table.get(kanji, 'locked')]
        draw.text((x, y), kanji, font=font, fill=color)

        x += font_size
        if x >= image_width - font_size:
            x = 0
            y += font_size

    image_io = StringIO()
    image.save(image_io, format="PNG")

    conn = S3Connection(settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY)
    bucket = Bucket(conn, settings.S3_BUCKET)
    key = Key(bucket)
    key.key = "images/{0}.png".format(hashlib.md5(api_key).hexdigest())
    key.set_contents_from_string(image_io.getvalue())
    key.set_acl('public-read')
    key.set_metadata('Content-Type', 'image/png')


