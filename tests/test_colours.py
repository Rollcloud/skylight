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


def test_colours_hcv():
    # from https://experilous.com/1/product/make-it-colorful/1.1/documentation/html/T_Experilous_MakeItColorful_ColorHCV.htm
    assert Colour(0, 0, 0).hcv == (0, 0, 0)  # black
    assert Colour(0, 0, 255).hcv == (255 * 2 / 3, 255, 255)  # blue
    assert Colour(0, 255, 255).hcv == (127, 255, 255)  # cyan
    assert Colour(127, 127, 127).hcv == (0, 0, 127)  # gray
    assert Colour(0, 255, 0).hcv == (255 / 3, 255, 255)  # green
    assert Colour(255, 0, 255).hcv == (255 * 5 / 6 - 0.5, 255, 255)  # magenta
    assert Colour(255, 0, 0).hcv == (0, 255, 255)  # red
    assert Colour(255, 255, 255).hcv == (0, 0, 255)  # white
    assert Colour(255, 255, 0).hcv == (255 / 6 - 0.5, 255, 255)  # yellow


def test_colours_from_hsv():
    assert Colour().from_hsv(0, 0, 0).hsv == (0, 0, 0)
    assert Colour().from_hsv(63, 127, 256).hsv == (63, 127, 255)
    assert Colour().from_hsv(255, 255, 255).hsv == (0, 255, 255)


def test_colours_from_hcv():
    assert Colour().from_hcv(0, 0, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(63, 127, 256).hcv == (63, 127, 255)
    assert Colour().from_hcv(255, 255, 255).hcv == (0, 255, 255)
    assert Colour().from_hcv(255, 0, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(0, 255, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(0, 0, 255).hcv == (0, 0, 255)
    assert Colour().from_hcv(127, 0, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(0, 127, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(0, 0, 127).hcv == (0, 0, 127)
    assert Colour().from_hcv(127, 127, 0).hcv == (0, 0, 0)
    assert Colour().from_hcv(0, 127, 127).hcv == (0, 127, 127)
    assert Colour().from_hcv(127, 0, 127).hcv == (0, 0, 127)


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
