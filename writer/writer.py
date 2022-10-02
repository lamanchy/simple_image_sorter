import asyncio
import logging
from os import environ
from os.path import abspath
from pathlib import Path

import nats
import webcolors
from pydantic import BaseModel, Extra, constr, validator, conbytes

BASE_DIR = Path(abspath(__file__)).parent
SORTED_IMAGES = BASE_DIR / 'sorted'

logging.basicConfig(level=environ['LOG_LEVEL'])
logger = logging.getLogger('writer')


class Headers(BaseModel, extra=Extra.forbid):
    name: constr(min_length=1)
    color: str

    @validator('color')
    def is_valid_color(cls, value):
        assert value in webcolors.HTML4_NAMES_TO_HEX.keys()


class Message(BaseModel):
    data: conbytes(min_length=1)
    headers: Headers


class Writer:
    @staticmethod
    def write_image(name, color, image):
        directory = SORTED_IMAGES / color
        directory.mkdir(exist_ok=True)

        with open(directory / name, 'wb') as file:
            file.write(image)

    async def handler(self, message):
        Message(data=message.data, headers=message.headers)
        image = message.data
        color = message.header['color']
        name = message.header['name']

        logger.info(f'storing image {name} with color {color}')
        self.write_image(name, color, image)

    async def subscribe(self, nc):
        await nc.subscribe('colored_images', cb=self.handler)


async def main():
    writer = Writer()

    nc = await nats.connect(environ['NATS_HOST'])
    await writer.subscribe(nc)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
    loop.run_forever()
