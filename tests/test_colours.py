from app.colours import Colour, brighten


def test_create_colours():
    assert Colour(0, 0, 0).colour == (0, 0, 0)
    assert Colour(63, 127, 256).colour == (63 / 255, 127 / 255, 1.0)
    assert Colour(255, 255, 255).colour == (1.0, 1.0, 1.0)


def test_colours_repr():
    assert repr(Colour(0, 0, 0)) == 'Colour(0, 0, 0)'
    assert repr(Colour(63, 127, 256)) == 'Colour(63, 127, 255)'
    assert repr(Colour(255, 255, 255)) == 'Colour(255, 255, 255)'


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


def test_colours_brighten():
    assert brighten(Colour(255, 0, 0), 0.5).hsv == (0, 255, 127)
    assert brighten(Colour(0, 255, 0), 0.5).hsv == (85, 255, 127)
    assert brighten(Colour(0, 0, 255), 0.5).hsv == (170, 255, 127)

    assert brighten(Colour(0, 255, 0), 0.0).rgb == (0, 0, 0)
    assert brighten(Colour(0, 255, 0), 0.5).rgb == (0, 127, 0)
    assert brighten(Colour(0, 255, 0), 1.0).rgb == (0, 255, 0)
    assert brighten(Colour(0, 255, 0), 2.0).rgb == (0, 255, 0)

    assert brighten(Colour(63, 127, 256), 0.1).hsv == (155, 192, 25)
    assert brighten(Colour(63, 127, 256), 0.5).hsv == (155, 192, 127)
    assert brighten(Colour(63, 127, 256), 1.0).hsv == (155, 192, 255)


def test_colours_brighten_copy():
    # check that original colour is not modified
    colour_a = Colour("#ffffff")
    colour_b = brighten(colour_a, 0.5)
    assert colour_a != colour_b


def test_colours_equivalence():
    assert Colour(255, 255, 255) == Colour(255, 255, 255)
    assert Colour(123, 124, 125) == Colour(123, 124, 125)
    assert Colour(255, 255, 255) == Colour("#ffffff")
    assert Colour(0, 0, 0) == Colour("#000000")
    assert Colour(0, 0, 0) != Colour(255, 255, 255)
