import time

from random import randrange

from colours import Colour


def lightning_flash(arduino, sky_colour=Colour(0, 0, 0), leds=range(60)):
    # Excerpt of original Arduino program from Storm_Cloud below:

    # const int lightPin = 3;

    # int rainCloud [25] [3] = {
    #  {256,256,256}, //white
    #  {0,0,0}, // off
    #  {100,100,150}, // slight blue
    #  {0,0,0}, // off
    #  {50,50,50}, // off
    #  {0,0,0}, // off
    #  {256,256,256}, //white
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {255,120,255}, // purple
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {100,100,150}, // slight blue
    #  {0,0,0}, // off
    #  {256,256,256}, //white
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {255,120,255}, // purple
    #  {0,0,0}, // off
    #  {0,0,0}, // off
    #  {256,256,256}, //white
    #  {50,50,50}, // off
    #  {0,0,0}, // off
    # };

    # void loop() {
    #   if(digitalRead(lightPin) == LOW) {
    #     for(int i=0; i< 10; i++) {
    #       runLightning();
    #     }
    #     for(int j=255,
    #   }
    #   delay(5);
    # }

    # void runLightning() {
    #     for(int i=0; i< 25; i++) {
    #     setRGB(rainCloud[i][0],rainCloud[i][1],rainCloud[i][2]);
    #     delay(random(30,250));
    #     if(i == 12) delay(random(250,1000));
    #   }
    #   delay(random(1000,5000));
    # }

    flash_sequence = [  # RGB
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
        sky_colour,  # off
        sky_colour,  # off
        Colour(100, 100, 150),  # slight blue
        sky_colour,  # off
        Colour(255, 255, 255),  # white
        sky_colour,  # off
        sky_colour,  # off
        sky_colour,  # off
        Colour(255, 120, 255),  # purple
        sky_colour,  # off
        sky_colour,  # off
        Colour(255, 255, 255),  # white
        Colour(50, 50, 50),  # off
        sky_colour,  # off
    ]

    for i, each in enumerate(flash_sequence):
        arduino.send_solid_range(each, leds)

        time.sleep(randrange(30, 250) / 1000)
        if i == 12:
            time.sleep(randrange(250, 1000) / 1000)

    # add delay of 1 sec - 5 sec before repeating
    # time.sleep(randrange(1, 5))


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
