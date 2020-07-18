# skylight
Mimic the lighting over the course of a day using Python, an Arduino, and a LED strip

## Requirements
* Python 3.8
* Arduino
* Programmable RGB LED strip

## Install
1. Wire up LED strip to power supply and Arduino
2. Use Pin 9 as the data pin to control the LEDs
3. Load `ino/parseserial.ino` onto the Arduino using the Arduino IDE
4. `$ cp docs/config/py app/config.py`
5. Replace the `SECRET_KEY` with an appropiate value
6. `$ pipenv sync`
7. `$ pipenv run app/serve.py`
8. Browse to `htp://localhost:5000` to control LEDs

## Test
`$ pipenv run python -m pytest ./tests`
