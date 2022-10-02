import asyncio
import logging
from os import environ

import cv2
import nats
import numpy as np
import webcolors
from pydantic import BaseModel, conbytes, Extra, constr
from webcolors import hex_to_rgb

logging.basicConfig(level=environ['LOG_LEVEL'])
logger = logging.getLogger('color_processor')


class Headers(BaseModel, extra=Extra.forbid):
    name: constr(min_length=1)


class Message(BaseModel):
    data: conbytes(min_length=1)
    headers: Headers


class ColorProcessor:
    @staticmethod
    def get_color_name(color):
        names, colors = zip(*webcolors.HTML4_NAMES_TO_HEX.items())
        colors = np.array([hex_to_rgb(hex) for hex in colors])
        distances = np.sqrt(np.sum((colors - color) ** 2, axis=1))
        index_of_smallest = np.where(distances == np.amin(distances))[0][0]
        return names[index_of_smallest]

    @staticmethod
    def get_color(image):
        decoded = cv2.imdecode(np.frombuffer(image, np.uint8), flags=1)
        brg_color = decoded.mean(axis=0).mean(axis=0).astype(int)
        return brg_color[::-1]

    async def handler(self, message, nc):
        Message(data=message.data, headers=message.headers)
        image = message.data

        logger.info(f'processing image {message.headers["name"]}')

        color = self.get_color(image)
        color_name = self.get_color_name(color)

        message.headers['color'] = color_name

        await nc.publish('colored_images', image, headers=message.headers)

    async def subscribe(self, nc):
        async def handler(message):
            await self.handler(message, nc)

        await nc.subscribe('new_images', cb=handler)


async def main():
    color_processor = ColorProcessor()

    nc = await nats.connect(environ['NATS_HOST'])
    await color_processor.subscribe(nc)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
