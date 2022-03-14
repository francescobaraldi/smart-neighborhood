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

<<<<<<< HEAD
unsigned long lasttime;

=======
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
void setup() {
  Serial.begin(9600);
  // Setup della comunicazione seriale con il bridge interno per ricevere i comandi per ogni servo
  finestra_nord.attach(finestra_nord_pin);
  finestra_nord.attach(finestra_sud_pin);
  // Setup dei push button dedicati all'azionamento manuale delle finestre (1 button per finestra)
  pinMode(button_sud_pin, INPUT);
  pinMode(button_nord_pin, INPUT);
<<<<<<< HEAD
  lasttime = millis();
}

void loop() {
  if (millis() - lasttime > 5000) {
	  lasttime = millis();
=======
}

void loop() {

  button_value_sud = digitalRead(button_sud_pin); // HIGH = button pressed (--> cambia stato della finestra sud), LOW = button released
  button_value_nord = digitalRead(button_nord_pin); // HIGH = button pressed (--> cambia stato della finestra nord), LOW = button released
  int pos_nord = finestra_nord.read();
  int pos_sud = finestra_sud.read();
  
  if (pos_nord == CLOSED || button_value_nord == HIGH) {
      Serial.write(0xff);
      Serial.write(0x01); // Lunghezza payload in byte
      Serial.write((char)(finestra_nord_pin));
      Serial.write(0xfe);
      for (; pos_nord < OPEN; pos_nord += 1) {
        finestra_nord.write(pos_nord);
        delay(15);
      }
    } else if (pos_nord == OPEN || button_value_nord == HIGH) {
      Serial.write(0xff);
      Serial.write(0x01); // Lunghezza payload in byte
      Serial.write((char)(finestra_nord_pin));
      Serial.write(0xfe);
      for (; pos_nord > CLOSED; pos_nord -= 1) {
        finestra_nord.write(pos_nord);
        delay(15);
      }
    }
    if (pos_sud == CLOSED || button_value_sud == HIGH) {
      Serial.write(0xff);
      Serial.write(0x01); // Lunghezza payload in byte
      Serial.write((char)(finestra_sud_pin));
      Serial.write(0xfe);
      for (; pos_sud < OPEN; pos_sud += 1) {
        finestra_sud.write(pos_sud);
        delay(15);
      }
    } else if (pos_sud == OPEN || button_value_sud == HIGH) {
      Serial.write(0xff);
      Serial.write(0x01); // Lunghezza payload in byte
      Serial.write((char)(finestra_sud_pin));
      Serial.write(0xfe);
      for (; pos_sud > CLOSED; pos_sud -= 1) {
        finestra_sud.write(pos_sud);
        delay(15);
      }
    }
  
  if (Serial.available() > 0) {
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
	  
	  // Leggere dati dal bridge (seriale) e in base agli stati ricevuti o alla pressione del push button aprire o chiudere le due finestre
	  // Dati ricevuti: stato per ogni servo (chiuso, aperto)
	  int new_pos_nord = Serial.read();
	  int new_pos_sud = Serial.read();
<<<<<<< HEAD
	  int pos_nord = finestra_nord.read();
	  int pos_sud = finestra_sud.read();
	  
	  button_value_sud = digitalRead(button_sud_pin); // HIGH = button pressed (--> cambia stato della finestra sud), LOW = button released
	  button_value_nord = digitalRead(button_nord_pin); // HIGH = button pressed (--> cambia stato della finestra nord), LOW = button released
	    
	  
	  if (new_pos_nord == OPEN && (pos_nord == CLOSED || button_value_nord == HIGH)) {
=======
	    
	  if (new_pos_nord == OPEN && pos_nord == CLOSED) {
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
	    for (; pos_nord < OPEN; pos_nord += 1) {
	      finestra_nord.write(pos_nord);
	      delay(15);
	    }
<<<<<<< HEAD
	  } else if (new_pos_nord == CLOSED && (pos_nord == OPEN || button_value_nord == HIGH)) {
=======
	  } else if (new_pos_nord == CLOSED && pos_nord == OPEN) {
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
	    for (; pos_nord > CLOSED; pos_nord -= 1) {
	      finestra_nord.write(pos_nord);
	      delay(15);
	    }
	  }
<<<<<<< HEAD
	  if (new_pos_sud == OPEN && (pos_sud == CLOSED || button_value_sud == HIGH)) {
=======
	  if (new_pos_sud == OPEN && pos_sud == CLOSED) {
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
	    for (; pos_sud < OPEN; pos_sud += 1) {
	      finestra_sud.write(pos_sud);
	      delay(15);
	    }
<<<<<<< HEAD
	  } else if (new_pos_sud == CLOSED && (pos_sud == OPEN || button_value_sud == HIGH)) {
=======
	  } else if (new_pos_sud == CLOSED && pos_sud == OPEN) {
>>>>>>> 0d94eea1054471e3dd6953f952d216cb4635472c
	    for (; pos_sud > CLOSED; pos_sud -= 1) {
	      finestra_sud.write(pos_sud);
	      delay(15);
	    }
	  }
  }
}
