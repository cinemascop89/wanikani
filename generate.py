# -*- coding: utf-8 -*-
import math

from PIL import Image, ImageFont, ImageDraw

import grid
WALLPAPER_SIZE = (1366, 768)


def generate_user_table(user_progress):

    table = {}
    for kanji in user_progress:
        stats = kanji['stats']
        if stats:
            table[kanji['character']] = stats['srs']

    return table

def generate_grid(user_progress):

    colors = {
        'apprentice':0xDD0093,
        'guru': 0x882D9E,
        'master': 0x94DDB,
        'enlighten': 0x0093DD,
        'burned': 0x434343,
        'locked': 0x101010,
    }

    user_table = generate_user_table(user_progress)
    image_width, image_height = WALLPAPER_SIZE
    font_size = int(math.sqrt(image_width * image_height / len(grid.kanji)))

    image = Image.new("RGB", WALLPAPER_SIZE)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("ipag.ttf", font_size, encoding='utf-8')

    y = 0

    for i, kanji in enumerate(grid.kanji):
        if i % (image_width / font_size) == 0:
            y += font_size
        position = (i * font_size % (image_width - 2), (i * font_size / image_width) * font_size)
        color = colors[user_table.get(kanji, 'locked')]

        draw.text(position, kanji, font=font, fill=color)

    return image

