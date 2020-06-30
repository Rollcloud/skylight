# skylight
Mimic the lighting over the course of a day using Python, an Arduino, and a LED strip

# Requirements
* Python 3.8
* Arduino
* Programmable RGB LED strip

# Install
1. Wire up LED strip to power supply and Arduino
2. Use Pin 9 as the data pin to control the LEDs
3. Load `ino/parseserial.ino` onto the Arduino using the Arduino IDE
4. `$ pipenv sync`
5. `$ pipenv run app/serve.py`
6. Browse to `htp://localhost:5000` to control LEDs

# Test
`$ pipenv run pytest ./tests`
