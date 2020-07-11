import random
import time

from math import ceil

from colours import Colour, brighten

FPS = 25


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

        time.sleep(1.0 / FPS)

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
