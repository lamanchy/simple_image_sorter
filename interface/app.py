import asyncio
from base64 import b64encode
from os import environ

import nats
from flask import Flask
from flask import render_template, request
from nats.errors import TimeoutError

app = Flask(__name__)


async def get_image_color(image):
    nc = await nats.connect(environ['NATS_HOST'])
    sub = await nc.subscribe("colored_images")
    await nc.publish('new_images', image, headers=dict(name='image'))

    try:
        message = await sub.next_msg(3)
    except TimeoutError:
        return 'Invalid image'

    return message.headers['color']


@app.route('/', methods=['GET', 'POST'])
def index(image_data=None):
    title = 'Simple image sorter'

    if request.method == 'POST':
        image = request.files['image'].read()

        image_url = b64encode(image).decode('ascii')
        image_color = asyncio.run(get_image_color(image))

    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run()
