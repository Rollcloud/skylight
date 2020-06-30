import random
import time

from colours import Colour


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
        arduino.send_solid_range(each, leds)
        time.sleep(random.randrange(5, 100) / 1000)

    # restore sky to original colour
    arduino.send_solid_range(sky_colour, leds)


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
