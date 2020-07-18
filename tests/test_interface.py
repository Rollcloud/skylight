from unittest.mock import call, patch, ANY

from app import interface as itf
from colours import Colour


class TestEncoding:
    def setup(self):
        self.leds = range(10)
        self.colours_prev = [Colour() for each in self.leds]

    def test_encode_differences(self):
        colours = [Colour() for each in self.leds]
        colours[2] = Colour("#123456")
        colours[4] = Colour("#789abc")

        colours, leds = itf.encode_differences(self.colours_prev, colours, self.leds)

        assert colours == [Colour("#123456"), Colour("#789abc")]
        assert leds == [2, 4]

    def test_encode_groups_simple(self):
        groups = itf.encode_groups(self.colours_prev, self.leds)

        assert list(groups) == [(Colour(), list(range(10)))]

    def test_encode_groups_complex(self):
        colours = [Colour() for each in self.leds]
        colours[2] = Colour("#123456")
        colours[4] = Colour("#789abc")
        colours[5] = Colour("#789abc")
        colours[6] = Colour("#789abc")

        groups = itf.encode_groups(colours, self.leds)

        assert list(groups) == [
            (Colour(), [0, 1]),
            (Colour("#123456"), [2]),
            (Colour(), [3]),
            (Colour("#789abc"), [4, 5, 6]),
            (Colour(), [7, 8, 9]),
        ]

    def test_encode(self):
        colours = [Colour() for each in self.leds]
        colours[2] = Colour("#123456")
        colours[4] = Colour("#789abc")
        colours[5] = Colour("#789abc")
        colours[6] = Colour("#789abc")

        groups = itf.encode(self.colours_prev, colours, self.leds)

        assert list(groups) == [
            (Colour("#123456"), [2]),
            (Colour("#789abc"), [4, 5, 6]),
        ]


# check results against argument into Arduino._send()
@patch('test_interface.itf.Arduino._send', autospec=True)
class TestArduino_send:
    def setup(self):
        self.arduino = itf.Arduino()

    def test_apply_leds(self, patched_send):
        self.arduino.apply_leds()
        patched_send.assert_called_with(ANY, ('A'), verbose=ANY)

    def test_clear_leds(self, patched_send):
        self.arduino.clear_leds()
        calls = [
            call(ANY, ('C'), verbose=ANY),
            call(ANY, ('A'), verbose=ANY),
        ]
        patched_send.assert_has_calls(calls, any_order=False)

    def test_set_colour_block(self, patched_send):
        self.arduino.set_colour_block(Colour("#12456"), range(10))
        patched_send.assert_called_with(ANY, ('G', 0, 9, 76, 232, 69), verbose=ANY)

    def test_set_leds_to_colours(self, patched_send):
        # check compression happens correctly
        new_colours = [Colour() for each in range(10)]
        new_colours[2] = Colour("#123456")
        new_colours[4] = Colour("#789abc")
        new_colours[5] = Colour("#789abc")
        new_colours[6] = Colour("#789abc")

        self.arduino.set_leds_to_colours(new_colours, range(10))

        calls = [
            call(ANY, ('G', 2, 2, 148, 201, 86), verbose=ANY),
            call(ANY, ('G', 4, 6, 148, 92, 188), verbose=ANY),
            call(ANY, ('A'), verbose=ANY),
        ]
        patched_send.assert_has_calls(calls, any_order=False)

        # check that previous led colours are remembered
        patched_send.reset_mock()
        new_colours[2] = Colour()

        self.arduino.set_leds_to_colours(new_colours, range(10))

        calls = [
            call(ANY, ('G', 2, 2, 0, 0, 0), verbose=ANY),
            call(ANY, ('A'), verbose=ANY),
        ]
        patched_send.assert_has_calls(calls, any_order=False)


# check results against argument into Arduino._send_str()
@patch('test_interface.itf.Arduino._send_str', autospec=True)
class TestArduino_send_str:
    def setup(self):
        self.arduino = itf.Arduino()

    def test_send_apply(self, patched_send_str):
        self.arduino._send(('A'))
        patched_send_str.assert_called_with(ANY, b'<A>', verbose=ANY)

    def test_send_clear(self, patched_send_str):
        self.arduino._send(('C'))
        patched_send_str.assert_called_with(ANY, b'<C>', verbose=ANY)

    def test_send_rgb(self, patched_send_str):
        self.arduino._send(('R', 50, 255, 0, 128))
        patched_send_str.assert_called_with(ANY, b'<R\x32\xff\x00\x80>', verbose=ANY)

    def test_send_hsv(self, patched_send_str):
        self.arduino._send(('H', 23, 255, 0, 128))
        patched_send_str.assert_called_with(ANY, b'<H\x17\xff\x00\x80>', verbose=ANY)


class TestArduinoSimulation:
    # check results against calls to Serial
    # any calls will result in an assertion fail
    def setup(self):
        self.arduino = itf.Arduino()
        self.arduino.connect(port=None)

    def test_apply_leds(self):
        self.arduino.apply_leds()
        assert hasattr(self.arduino, 'ser') is False

    def test_clear_leds(self):
        self.arduino.clear_leds()
        assert hasattr(self.arduino, 'ser') is False

    def test_set_colour_block(self):
        self.arduino.set_colour_block(Colour("#12456"), range(10))
        assert hasattr(self.arduino, 'ser') is False

    def test_set_leds_to_colours(self):
        new_colours = [Colour() for each in range(10)]
        self.arduino.set_leds_to_colours(new_colours, range(10))
        assert hasattr(self.arduino, 'ser') is False
