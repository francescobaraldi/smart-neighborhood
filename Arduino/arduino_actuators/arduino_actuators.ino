#include <Servo.h>

const int finestra_nord_pin = 8;
const int finestra_sud_pin = 9;

Servo finestra_nord;
Servo finestra_sud;

#define OPEN 0
#define CLOSED 1

void setup() {
  Serial.begin(9600);
  // Setup della comunicazione seriale con il bridge interno per ricevere i comandi per ogni servo
  finestra_nord.attach(finestra_nord_pin);
  finestra_nord.attach(finestra_sud_pin);
}

void loop() {
  // Leggere dati dal bridge (seriale) e in base agli stati ricevuti aprire o chiudere le due finestre
  // Dati ricevuti: stato per ogni servo (chiuso, aperto)
  int new_pos_nord = Serial.read();
  int new_pos_sud = Serial.read();
  int pos_nord = finestra_nord.read();
  int pos_sud = finestra_sud.read();
  if (new_pos_nord == OPEN && pos_nord == CLOSED) {
    for (; pos_nord < OPEN; pos_nord += 1) {
      finestra_nord.write(pos_nord);
      delay(15);
    }
  } else if (new_pos_nord == CLOSED && pos_nord == OPEN) {
    for (; pos_nord > CLOSED; pos_nord -= 1) {
      finestra_nord.write(pos_nord);
      delay(15);
    }
  }
  if (new_pos_sud == OPEN && pos_sud == CLOSED) {
    for (; pos_sud < OPEN; pos_sud += 1) {
      finestra_sud.write(pos_sud);
      delay(15);
    }
  } else if (new_pos_sud == CLOSED && pos_sud == OPEN) {
    for (; pos_sud > CLOSED; pos_sud -= 1) {
      finestra_sud.write(pos_sud);
      delay(15);
    }
  }
}
