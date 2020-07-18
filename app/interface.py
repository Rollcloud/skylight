from itertools import groupby
from math import ceil
from time import sleep
from time import time as now
from typing import Iterator, List, Tuple

from serial import Serial
from colored import bg, stylize

from colours import Colour

TIME_BETWEEN_CMDS = 0.010  # s
TIME_BETWEEN_APPLIES = 0.030  # s

LEDS = range(60)  # must start from 0


def linspace(start, stop, num=10):
    return [start + x * (stop - start) / (num - 1) for x in range(num)]


def transpose(array):
    return [list(each) for each in zip(*array)]


def encode_differences(colours_prev, colours, leds):
    if colours_prev is None:
        colours_prev = colours

        return colours, leds

    diff = []
    for p, c, l in zip(colours_prev, colours, leds):
        if p != c:
            diff.append((c, l))

    colours_prev = colours

    return transpose(diff)


def encode_groups(colours, leds) -> Iterator[Tuple[Colour, List[int]]]:
    '''returns a list of colour-led ranges using 'absolute' run length encoding'''

    def key_func(i):
        return i[0]

    groups = (
        (key, [l for c, l in group])
        for key, group in groupby(list(zip(colours, leds)), key_func)
    )

    return groups


def encode(colours_prev, colours, leds) -> Iterator[Tuple[Colour, List[int]]]:
    '''encode by both differences and groups'''
    return encode_groups(*encode_differences(colours_prev, colours, leds))


class Arduino:
    block_until = 0
    led_colours = [Colour() for each in LEDS]
    simulate = False

    def connect(self, port=None, baud=9600, acknowledge=False, verbose=False):
        if verbose:
            print(f"Connecting to '{PORT}' at {baud} baud...")

        if port is None:
            self.simulate = True

        if self.simulate:
            print("Connected to Arduino (simulated)")
        else:
            self.ser = Serial(port, baud, timeout=5)

            try:
                if b'ready' in self.ser.readline():
                    if acknowledge:
                        self.clear_leds()
                return True
            except self.ser.SerialTimeoutException:
                print("Data could not be read")

    def disconnect(self):
        if self.simulate:
            print("Closing connection")
        else:
            if self.ser:
                self.ser.close()

    def print_leds(self):
        output = ''
        for colour in self.led_colours:
            output += stylize(" ", bg(colour.hex))

        print(output)

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
            sleep(TIME_BETWEEN_CMDS)

        try:
            self._send_str(
                b'<' + bytes((ord(command[0]),) + command[1:]) + b'>', verbose=verbose
            )
        except TypeError:  # for command letter only with no parameters
            self._send_str(b'<' + bytes([ord(command[0])]) + b'>', verbose=verbose)

    def apply_leds(self, verbose=False):
        if self.simulate:
            self.print_leds()
        else:
            self._send(('A'), verbose=verbose)
            self.block_until = now() + TIME_BETWEEN_APPLIES

    def clear_leds(self, verbose=False):
        if self.simulate:
            self.print_leds()
        else:
            self._send(('C'), verbose=verbose)
            self.apply_leds(verbose=verbose)
        self.led_colours = [Colour() for each in LEDS]

    def set_colour_block(self, colour: Colour, leds: List[int] = LEDS, verbose=False):
        '''
        Sends commands directly over serial
        '''
        if self.simulate:
            pass
        else:
            led_min = leds[0]
            led_max = leds[-1]
            self._send(('G', led_min, led_max, *colour.hsv), verbose=verbose)

    def set_leds_to_colours(
        self, new_colours: List[Colour], leds: List[int] = LEDS, verbose=False
    ):
        '''
        Encodes LED commands to reduce serial communications
        '''
        groups = encode(self.led_colours, new_colours, leds)
        for c, l in groups:
            self.set_colour_block(c, l, verbose=verbose)

        # remember colours for next command
        for n, l in zip(new_colours, leds):
            self.led_colours[l] = n

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
            self.set_leds_to_colours([Colour().from_hsv(h, s, v)] * len(leds), leds)
            sleep(1.0 / fps)
