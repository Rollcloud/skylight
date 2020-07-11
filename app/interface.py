from math import ceil
from time import sleep
from time import time as now
from typing import List, Tuple

from serial import Serial

from colours import Colour

PORT = 'COM3'
BAUD = 9600

LEDS = range(60)


def linspace(start, stop, num=10):
    return [start + x * (stop - start) / (num - 1) for x in range(num)]


class Arduino:
    block_until = 0

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

    def _send_str(self, command: bytes, verbose=False, read_nack=False):
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

    def _send(self, command: Tuple, verbose=False):
        """
        Convert a command-tuple to a command-string
        eg: (R, 255, 0, 128) -> b"R\xFF\x00\x80"
        """
        # wait for strip to write previous command before sending next command
        while now() < self.block_until:
            sleep(0.015)  # 10 ms

        try:
            self._send_str(
                b'<' + bytes((ord(command[0]),) + command[1:]) + b'>', verbose=verbose
            )
        except TypeError:  # for command letter only with no parameters
            self._send_str(b'<' + bytes([ord(command[0])]) + b'>', verbose=verbose)

    def apply_leds(self, verbose=False):
        self._send(('A'), verbose=verbose)
        self.block_until = now() + 0.100  # 100 ms

    def clear_leds(self, verbose=False):
        self._send(('C'), verbose=verbose)
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

    def fade_from_to(
        self, colour_old, colour_new, leds: List[int] = LEDS, time=1.00, fps=10
    ):
        frames = int(ceil(fps * time))
        h_old, s_old, v_old = colour_old.hsv
        h_new, s_new, v_new = colour_new.hsv

        for h, s, v in zip(
            linspace(h_old, h_new, frames),
            linspace(s_old, s_new, frames),
            linspace(v_old, v_new, frames),
        ):
            print(Colour().from_hsv(h, s, v).hsv)
            self.send_solid_range(Colour().from_hsv(h, s, v), leds)
            # sleep(1.0 / fps)
