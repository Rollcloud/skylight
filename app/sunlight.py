import time

import interface as ard

FPS = 30
LEDS = range(35, 60)


def loop():
    for h in range(0, 255):
        colour = (h, 255, 255)
        ard.send_solid_range(colour, LEDS, col_type='HSV', verbose=False)
        time.sleep(1 / FPS)


def main():
    ard.connect()

    print("Running...")

    while True:
        loop()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Aborting...")
        ard.send(('C'))
        ard.send(('A'))
