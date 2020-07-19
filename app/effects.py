import random
import time

from math import ceil

from colours import Colour, brighten
from typing import List

FPS = 25


def linspace(start, stop, num=10):
    return [start + x * (stop - start) / (num - 1) for x in range(num)]


class Cloud:
    def __init__(self, position, width=25, edge=5, opacity=0.3):
        '''
        position: initial position of cloud
        width: of cloud shadow in LEDs
        edge: num LEDs per side in penumbra of cloud shadow
        opacity: strength of cloud shadow (0, 1)

        model - an animated block moving to the right
          _____________
         /            /  ->
        /____________/
        E             E
        |<-  width  ->|
             position |
        '''
        self.position = position

        self.width = width
        self.edge = edge
        self.opacity = opacity

    def opacity_at(self, x):
        # model
        # 0.3    _______
        # y     /       \
        # 0 ___/    x    \|

        edge = self.edge
        width = self.width
        opacity = self.opacity

        x -= self.position

        if x > -width + edge and x < -edge:
            # in middle
            return opacity
        elif x >= -width and x <= -width + edge:
            # left limb
            # y= opacity / edge * x + opacity / edge * width
            return opacity / edge * x + opacity / edge * width
        elif x >= -edge and x <= 0:
            # right limb
            # y= - opacity / edge * x
            return -opacity / edge * x
        else:
            # clear sky
            return 0

    def calc_colours(self, leds, sky_colour):
        return [brighten(sky_colour, 1 - self.opacity_at(i)) for i in leds]


def cloud_drift(
    arduino, sky_colour=Colour(0, 0, 0), leds=range(60), velocity=5,
):
    '''
    velocity: velocity of cloud shadow in LEDs / second
    '''
    CLOUD_WIDTH = 25

    start_position = leds[0] if velocity > 0 else leds[-1] + CLOUD_WIDTH

    cloud = Cloud(start_position, CLOUD_WIDTH, opacity=0.75)

    seconds = abs((len(leds) + CLOUD_WIDTH) / velocity)
    frames = int(ceil(FPS * seconds))

    print(seconds, frames)

    for each in range(frames):
        cloud.position += velocity / FPS

        colours = cloud.calc_colours(leds, sky_colour)
        arduino.set_leds_to_colours(colours, leds)

        time.sleep(1.0 / FPS - 0.050)

    # restore sky to original colour
    arduino.set_leds_to_colours([sky_colour] * len(leds), leds)


def lightning_flash(arduino, sky_colour=Colour(0, 0, 0), leds=range(60)):
    # Based on the Storm_Cloud Arduino sketch:

    flash_sequences = (
        [  # RGB
            Colour(255, 255, 255),  # white
            sky_colour,  # off
            Colour(100, 100, 150),  # slight blue
            sky_colour,  # off
            Colour(50, 50, 50),  # off
            sky_colour,  # off
            Colour(255, 255, 255),  # white
            sky_colour,  # off
            sky_colour,  # off
            sky_colour,  # off
            Colour(255, 120, 255),  # purple
        ],
        [
            Colour(100, 100, 150),  # slight blue
            sky_colour,  # off
            Colour(255, 255, 255),  # white
            sky_colour,  # off
            sky_colour,  # off
            Colour(255, 120, 255),  # purple
            sky_colour,  # off
            sky_colour,  # off
            Colour(255, 255, 255),  # white
            sky_colour,  # off
            Colour(50, 50, 50),  # off
        ],
        [
            Colour(255, 200, 120),  # orange
            sky_colour,  # off
            sky_colour,  # off
            sky_colour,  # off
            Colour(255, 255, 255),  # white
            sky_colour,  # off
            Colour(255, 120, 255),  # purple
            sky_colour,  # off
            Colour(50, 50, 50),  # off
            sky_colour,  # off
            Colour(200, 150, 100),  # slight orange
        ],
    )

    for i, each in enumerate(random.choice(flash_sequences)):
        arduino.set_leds_to_colours([each] * len(leds), leds)
        time.sleep(random.randrange(5, 100) / 1000)

    # restore sky to original colour
    arduino.set_leds_to_colours([sky_colour] * len(leds), leds)


def rect(r, theta):
    '''
    theta in degrees
    returns tuple; (float, float); (x,y)
    '''
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def polar(x, y):
    '''
    returns r, theta(degrees)
    '''
    r = (x ** 2 + y ** 2) ** 0.5
    theta = math.degrees(math.atan2(y, x))
    return r, theta


def hcv_to_xyz(h, c, v):
    r, theta = c, h / 255 * 360
    return (*rect(), v)


def xyz_to_hcv(x, y, z):
    r, theta = polar(x, y)
    theta = theta / 360 * 255
    return (r, theta, v)


def fade_from_to(
    arduino, colour_old, colour_new, leds: List[int] = range(60), duration=1.00
):
    '''
    create a gradient through a cone in cartesian space
    '''
    frames = int(ceil(FPS * duration))

    x1, y1, z1 = hcv_to_xyz(*colour_old.hcv)
    x2, y2, z2 = hcv_to_xyz(*colour_new.hcv)

    for x, y, z in zip(
        linspace(x1, x2, frames), linspace(y1, y2, frames), linspace(z1, z2, frames)
    ):
        # x, y, z -> hcv -> hsv
        c = Colour().from_hcv(xyz_to_hcv(x, y, z))

        arduino.set_leds_to_colours([c] * len(leds), leds)
        time.sleep(1.0 / FPS)


def main():
    from interface import Arduino

    arduino = Arduino()

    try:
        arduino.connect(baud=19200)
        lightning_flash(arduino)
    except KeyboardInterrupt:
        print("Aborting...")
        arduino.send(('C'))
        arduino.send(('A'))
        arduino.disconnect()


if __name__ == '__main__':
    main()
