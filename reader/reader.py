import asyncio
import logging
from asyncio import run
from os import environ
from os.path import abspath
from pathlib import Path
from time import time

import nats

BASE_DIR = Path(abspath(__file__)).parent
IMAGES_SOURCE = BASE_DIR / 'source'

logging.basicConfig(level=environ['LOG_LEVEL'])
logger = logging.getLogger('reader')


class Reader:
    def __init__(self, *, upload_all=False):
        self.since_time = 0 if upload_all else time()
        self.refresh_interval = 1

    def get_new_images(self):
        for file in IMAGES_SOURCE.iterdir():
            if file.name == '.gitkeep':
                continue

            if file.stat().st_mtime > self.since_time:
                yield file

    def set_since_time(self):
        self.since_time = time()

    async def get_images(self):
        while True:
            new_images = list(self.get_new_images())
            self.set_since_time()

            # no yield from in async functions :(
            for image in new_images:
                yield image

            await asyncio.sleep(self.refresh_interval)


async def main():
    reader = Reader(upload_all=True)

    nc = await nats.connect(environ['NATS_HOST'])

    async for image in reader.get_images():
        with open(image, 'rb') as f:
            logger.info(f'New image {image.name}')
            await nc.publish('new_images', f.read(), headers=dict(name=image.name))


if __name__ == '__main__':
    run(main())
