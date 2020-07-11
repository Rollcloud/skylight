from unittest.mock import call, patch, ANY

from app import interface as itf


class TestEncoding:
    def test_encode_differences(self):
        pass

    def test_encode_groups(self):
        pass

    def test_encode(self):
        pass


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
