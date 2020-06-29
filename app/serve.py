#! .venv/bin/python3

# Start with a basic flask app webpage.
from flask_socketio import SocketIO
from flask import Flask, render_template

# import LED packages
import effects
from interface import Arduino

# constants
LEDS = range(35, 60)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

g = {}

# turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)


def get_arduino():
    global g

    if 'arduino' not in g:
        print(" *** Connecting to Arduino ***")
        g['arduino'] = Arduino()
        g['arduino'].connect(baud=19200)

    # for each in g:
    #     print(each)

    return g['arduino']


def close_arduino(e=None):
    global g

    if 'arduino' in g:
        print(" *** Disconnecting from Arduino ***")
        g['arduino'].close()


@app.route('/')
def index():
    # only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')


@socketio.on('connect')
def test_connect():
    print('Client connected')
    get_arduino()


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')
    close_arduino()


@socketio.on('json')
def handle_json(json):
    # print('received json: ' + str(json))

    def scale(old_value, old_min, old_max, new_min, new_max):
        return int(
            ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min)
            + new_min
        )

    colour_in = json['data']
    colour_out = (
        scale(colour_in['h'], 0, 360, 0, 255),
        scale(colour_in['s'], 0, 100, 0, 255),
        scale(colour_in['v'], 0, 100, 0, 255),
    )
    # print(colour_out)
    get_arduino().send_solid_range(colour_out, LEDS, col_type='HSV')


@socketio.on('effect')
def handle_effect(json):
    # print('received json: ' + str(json))

    effect = json['effect']

    if effect == 'lightning':
        effects.lightning_flash(get_arduino(), leds=LEDS)


if __name__ == '__main__':
    socketio.run(app)
