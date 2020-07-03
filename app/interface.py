from time import sleep
from typing import List, Tuple

from serial import Serial

from colours import Colour

PORT = 'COM3'
BAUD = 9600

LEDS = range(60)


class Arduino:
    def connect(self, port=PORT, baud=BAUD, acknowledge=False, verbose=False):
        if verbose:
            print(f"Connecting to '{PORT}' at {baud} baud...")

        self.ser = Serial(port, baud, timeout=5)

        try:
            if b'ready' in self.ser.readline():
                if acknowledge:
                    self.clear_leds()
            return True
        except self.ser.SerialTimeoutException:
            print("Data could not be read")

    def disconnect(self):
        if self.ser:
            self.ser.close()

    def send_str(self, command: bytes, verbose=False, read_nack=False):
        """
        Commands:
        C: clear all lights to black
        A: apply all lights as set
        R: set a specific LED to a RGB colour
        H: set a specific LED to a HSV colour
        """
        if verbose:
            print(f"Sending {command}")

        self.ser.write(command)

        # Read back negative acknowledge, will use timeout
        # Data only provide if command not recognised
        if read_nack:
            try:
                print("Reading...")
                print(self.ser.readline())
            except self.ser.SerialTimeoutException:
                print("Data could not be read")

    def send(self, command: Tuple, verbose=False):
        """
        Convert a command-tuple to a command-string
        eg: (R, 255, 0, 128) -> b"R\xFF\x00\x80"
        """
        try:
            self.send_str(
                b'<' + bytes((ord(command[0]),) + command[1:]) + b'>', verbose=verbose
            )
        except TypeError:  # for command letter only with no parameters
            self.send_str(b'<' + bytes([ord(command[0])]) + b'>', verbose=verbose)

    def apply_leds(self, verbose=False):
        self.send(('A'), verbose=verbose)

    def clear_leds(self, verbose=False):
        self.send(('C'), verbose=verbose)
        self.apply_leds(verbose=verbose)

    def send_solid_range(self, colour: Colour, leds: List[int] = LEDS, verbose=False):
        for idx in leds:
            self.send(('R', idx, *colour.rgb), verbose=verbose)
        self.apply_leds(verbose=verbose)

    def set_leds_to_colours(
        self, colours: List[Colour], leds: List[int] = LEDS, verbose=False
    ):
        for idx, c in zip(leds, colours):
            self.send(('R', idx, *c.rgb), verbose=verbose)
        self.apply_leds(verbose=verbose)


def main():
    arduino = Arduino()
    arduino.connect(PORT, 19200)

    while True:
        arduino.send_str(b'<A\x07\x23\x73>')
        sleep(1)
        arduino.send(('R', 50, 255, 0, 128))
        sleep(1)
        arduino.send(('C'))
        sleep(1)

        for i in range(40, 60):
            arduino.send(('C'))
            arduino.send(('H', i, 255, 0, 128))
            arduino.send(('A'))
            sleep(1)


if __name__ == "__main__":
    main()
