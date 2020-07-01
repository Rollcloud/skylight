#! .venv/bin/python3

# Start with a basic flask app webpage.
from flask_socketio import SocketIO
from flask import Flask, render_template

# import LED packages
import effects

from colours import Colour
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
    global g
    # print('received json: ' + str(json))

    colour = Colour(json['data'])
    # print(colour.rgb)

    g['sky_colour'] = colour
    get_arduino().send_solid_range(colour, LEDS)


@socketio.on('effect')
def handle_effect(json):
    global g

    if 'sky_colour' not in g:
        g['sky_colour'] = Colour(0, 0, 0)

    if json['effect'] == 'lightning':
        effects.lightning_flash(get_arduino(), g['sky_colour'], leds=LEDS)

    if json['effect'] == 'cloud_drift':
        effects.cloud_drift(get_arduino(), g['sky_colour'], leds=LEDS)


if __name__ == '__main__':
    socketio.run(app)
