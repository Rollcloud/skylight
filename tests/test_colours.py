import sys

sys.path.append(".")

from app.colours import Colour  # noqa


def test_create_colours():
    assert Colour(0, 0, 0).colour == (0, 0, 0)
    assert Colour(63, 127, 256).colour == (63 / 255, 127 / 255, 1.0)
    assert Colour(255, 255, 255).colour == (1.0, 1.0, 1.0)


def test_colours_hex():
    assert Colour(0, 0, 0).hex == "#000000"
    assert Colour(63, 127, 256).hex == "#3f7fff"
    assert Colour(255, 255, 255).hex == "#ffffff"


def test_colours_rgb():
    assert Colour(0, 0, 0).rgb == (0, 0, 0)
    assert Colour(63, 127, 256).rgb == (63, 127, 255)
    assert Colour(255, 255, 255).rgb == (255, 255, 255)


def test_colours_hsv():
    assert Colour(0, 0, 0).hsv == (0, 0, 0)
    assert Colour(63, 127, 256).hsv == (155, 192, 255)
    assert Colour(255, 255, 255).hsv == (0, 0, 255)