import time

from typing import Tuple

from serial import Serial

PORT = 'COM3'
BAUD = 9600


def connect(PORT=PORT, BAUD=BAUD, verbose=False):
    global s

    if verbose:
        print(f"Connecting to '{PORT}' at {BAUD} baud")
    s = Serial(PORT, BAUD, timeout=1)


def send_str(command: bytes, verbose=False):
    """
    Commands:
    C: clear all lights to black
    A: apply all lights as set
    R: set a specific LED to a RGB colour
    H: set a specific LED to a HSV colour
    """
    global s

    if verbose:
        print(f"Sending {command}")

    s.write(command)

    # Read back echo
    if verbose:
        try:
            print("Reading...")
            print(s.readline())
        except s.SerialTimeoutException:
            print("Data could not be read")


def send(command: Tuple, verbose=False):
    """
    Convert a command-tuple to a command-string
    eg: (R, 255, 0, 128) -> b"R\xFF\x00\x80"
    """
    try:
        send_str(b'<' + bytes((ord(command[0]),) + command[1:]) + b'>', verbose=verbose)
    except TypeError:  # for command letter only with no parameters
        send_str(b'<' + bytes([ord(command[0])]) + b'>', verbose=verbose)


def send_solid_range(colour, leds, col_type='HSV', verbose=False):
    for idx in leds:
        send((col_type[0], idx, *colour), verbose=verbose)
    send(('A'), verbose=verbose)


def main():
    connect(PORT, BAUD)

    while True:
        send_str(b'<A\x07\x23\x73>')
        time.sleep(1)
        send(('R', 50, 255, 0, 128))
        time.sleep(1)
        send(('C'))
        time.sleep(1)

        for i in range(40, 60):
            send(('C'))
            send(('H', i, 255, 0, 128))
            send(('A'))
            time.sleep(1)


if __name__ == "__main__":
    main()
