from pathlib import Path

import pytest

from color_processor import ColorProcessor


def test_get_color_name():
    assert ColorProcessor.get_color_name([0, 0, 0]) == 'black'
    assert ColorProcessor.get_color_name([0, 0, 1]) == 'black'
    assert ColorProcessor.get_color_name([300, 300, 300]) == 'white'

    # test order
    assert ColorProcessor.get_color_name([0, 0, 255]) == 'blue'
    with pytest.raises(ValueError):
        ColorProcessor.get_color_name([20, 10, 20, 0])


def test_get_color():
    directory = Path(__file__).parent / 'test_images'
    with open(directory / '__valid_test_image.png', 'rb') as image:
        color = ColorProcessor.get_color(image.read())
        assert list(color) == [63, 72, 204]

    with open(directory / '__invalid_test_image.png', 'rb') as image:
        with pytest.raises(AttributeError):
            ColorProcessor.get_color(image.read())
