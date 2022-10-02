import shutil
from os import remove
from os.path import exists
from pathlib import Path
from time import time, sleep

import pytest

images_dir = Path('images')


def remove_file(path):
    try:
        remove(path)
    except FileNotFoundError:
        pass


def clean_image(name, color):
    remove_file(images_dir / 'source' / name)
    remove_file(images_dir / 'sorted' / color / name)


def wait_until(condition, timeout=1):
    start = time()
    while not condition():
        if time() - start > timeout:
            raise TimeoutError

        sleep(0.1)


@pytest.fixture()
def valid_image():
    name = '__valid_test_image.png'
    color = 'blue'
    clean_image(name, color)
    yield name, color
    clean_image(name, color)


@pytest.fixture()
def invalid_image():
    name = '__invalid_test_image.png'
    color = 'none'
    clean_image(name, color)
    yield name, color
    clean_image(name, color)


def test_valid_image(valid_image):
    name, color = valid_image
    shutil.copy(images_dir / 'test_images' / name, images_dir / 'source')

    fn = lambda: exists(images_dir / 'sorted' / color / name)

    wait_until(fn)


def test_invalid_image(invalid_image):
    name, color = invalid_image
    shutil.copy(images_dir / 'test_images' / name, images_dir / 'source')

    fn = lambda: exists(images_dir / 'sorted' / color / name)

    with pytest.raises(TimeoutError):
        wait_until(fn)
