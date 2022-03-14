#include <Servo.h>

const int finestra_nord_pin = 8;
const int finestra_sud_pin = 9;
const int button_sud_pin = 2; // azionamento manuale scuri finestra sud
const int button_nord_pin = 3; // azionamento manuale scuri finestra nord

Servo finestra_nord;
Servo finestra_sud;
bool button_value_sud;
bool button_value_nord;

#define OPEN 0
#define CLOSED 1

unsigned long lasttime;

void setup() {
  Serial.begin(9600);
  // Setup della comunicazione seriale con il bridge interno per ricevere i comandi per ogni servo
  finestra_nord.attach(finestra_nord_pin);
  finestra_nord.attach(finestra_sud_pin);
  // Setup dei push button dedicati all'azionamento manuale delle finestre (1 button per finestra)
  pinMode(button_sud_pin, INPUT);
  pinMode(button_nord_pin, INPUT);
  lasttime = millis();
}

void loop() {
  if (millis() - lasttime > 5000) {
	  lasttime = millis();
	  
	  // Leggere dati dal bridge (seriale) e in base agli stati ricevuti o alla pressione del push button aprire o chiudere le due finestre
	  // Dati ricevuti: stato per ogni servo (chiuso, aperto)
	  int new_pos_nord = Serial.read();
	  int new_pos_sud = Serial.read();
	  int pos_nord = finestra_nord.read();
	  int pos_sud = finestra_sud.read();
	  
	  button_value_sud = digitalRead(button_sud_pin); // HIGH = button pressed (--> cambia stato della finestra sud), LOW = button released
	  button_value_nord = digitalRead(button_nord_pin); // HIGH = button pressed (--> cambia stato della finestra nord), LOW = button released
	    
	  
	  if (new_pos_nord == OPEN && (pos_nord == CLOSED || button_value_nord == HIGH)) {
	    for (; pos_nord < OPEN; pos_nord += 1) {
	      finestra_nord.write(pos_nord);
	      delay(15);
	    }
	  } else if (new_pos_nord == CLOSED && (pos_nord == OPEN || button_value_nord == HIGH)) {
	    for (; pos_nord > CLOSED; pos_nord -= 1) {
	      finestra_nord.write(pos_nord);
	      delay(15);
	    }
	  }
	  if (new_pos_sud == OPEN && (pos_sud == CLOSED || button_value_sud == HIGH)) {
	    for (; pos_sud < OPEN; pos_sud += 1) {
	      finestra_sud.write(pos_sud);
	      delay(15);
	    }
	  } else if (new_pos_sud == CLOSED && (pos_sud == OPEN || button_value_sud == HIGH)) {
	    for (; pos_sud > CLOSED; pos_sud -= 1) {
	      finestra_sud.write(pos_sud);
	      delay(15);
	    }
	  }
  }
}
