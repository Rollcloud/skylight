// Original source: https://forum.arduino.cc/index.php?topic=396450.0
// Example 6 - Receiving binary data

#include <FastLED.h>
#define NUM_LEDS 60
#define DATA_PIN 9
#define BAUD 19200

CRGBArray<NUM_LEDS> leds;

const byte NUM_BYTES = 32;

byte receivedBytes[NUM_BYTES];
byte numReceived = 0;

boolean newData = false;

void setup() {
  delay(3000); // power-up safety delay
  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS).setCorrection(TypicalSMD5050);
  FastLED.setTemperature(DirectSunlight);

  Serial.begin(BAUD);
  Serial.println("<Arduino is ready>");
}

void loop() {
  recvBytesWithStartEndMarkers();
  showNewData();
}

void setLedHSV(byte command[]) {
  int idx = command[1];
  byte hue = command[2];
  byte sat = command[3];
  byte val = command[4];

  leds[command[1]] = CHSV(hue, sat, val);
}

void setRangeHSV(byte command[]) {
  int min = command[1];
  int max = command[2];
  byte hue = command[3];
  byte sat = command[4];
  byte val = command[5];

  for (int i = min; i <= max; ++i) {
    leds[i] = CHSV(hue, sat, val);
  }
}

void setLedRGB(byte command[]) {
  int idx = command[1];
  byte red = command[2];
  byte grn = command[3];
  byte blu = command[4];

  leds[command[1]] = CRGB(red, grn, blu);
}

void recvBytesWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  byte startMarker = 0x3C;
  byte endMarker = 0x3E;
  byte rb;


  while (Serial.available() > 0 && newData == false) {
    rb = Serial.read();

    if (recvInProgress == true) {
      if (rb != endMarker) {
        receivedBytes[ndx] = rb;
        ndx++;
        if (ndx >= NUM_BYTES) {
          ndx = NUM_BYTES - 1;
        }
      } else {
        receivedBytes[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        numReceived = ndx;  // save the number for use when printing
        ndx = 0;
        newData = true;
      }
    }

    else if (rb == startMarker) {
      recvInProgress = true;
    }
  }
}

void showNewData() {
  if (newData == true) {
    // Commands:
    // C: clear all lights to black
    // A: apply all lights as set
    // R: set a specific LED to a RGB colour
    // H: set a specific LED to a HSV colour

    switch (char(receivedBytes[0])) {
    case 'C':
      FastLED.clear();
      break;
    case 'A':
      FastLED.show();
      break;
    case 'G':
      setRangeHSV(receivedBytes);
      break;
    case 'H':
      setLedHSV(receivedBytes);
      break;
    case 'R':
      setLedRGB(receivedBytes);
      break;
    default:
      // if nothing else matches, do the default (optional)

      // Print incoming command
      Serial.print("This just in (HEX values)... ");

      Serial.print(char(receivedBytes[0]));
      Serial.print(' ');

      for (byte n = 1; n < numReceived; n++) {
        Serial.print(receivedBytes[n], HEX);
        Serial.print(' ');
      }

      Serial.println();

      break;
    }

    newData = false;
  }
}
