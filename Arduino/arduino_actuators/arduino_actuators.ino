#include <Servo.h>

const int finestra_nord_pin = 8;
const int finestra_sud_pin = 8;

Servo finestra_nord;
Servo finestra_sud;

void setup() {
  finestra_nord.attach(finestra_nord_pin);
  finestra_nord.attach(finestra_sud_pin);
}

void loop() {
  finestra_nord.write (-180);
  delay (500);
  finestra_nord.write (-150);
  delay (500);
  finestra_nord.write (-120);
  delay (500);
  finestra_nord.write (-90);
  delay (500);
  finestra_nord.write (-60);
  delay (500);
  finestra_nord.write (-30);
  delay (500);
  finestra_nord.write (0);
  delay (500);
  finestra_nord.write (30);
  delay (500);
  finestra_nord.write (60);
  delay (500);
}
