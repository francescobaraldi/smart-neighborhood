#include <Servo.h>

#define DEBOUNCING_TIME 100
#define OPEN_NORD 179
#define CLOSED_NORD 90
#define OPEN_SUD 90
#define CLOSED_SUD 180
#define OPEN 1
#define CLOSED 0

enum states {
  S0, S1, S2
};

enum input_symbols {
  PRESSED,
  RELEASED
};

enum output_symbols {
  MOVE,
  NOT_MOVE
};

const int finestra_nord_pin = 8;  // servo Hitec
const int finestra_sud_pin = 9;   // servo TowerPro
const int button_nord_pin = 2;    // azionamento manuale scuri finestra nord
const int button_sud_pin = 3;     // azionamento manuale scuri finestra sud

int current_nord_button_value;
int current_sud_button_value;
states current_state_nord;
states current_state_sud;
unsigned long last_change_time;

Servo finestra_nord;
Servo finestra_sud;

void setup() {
  Serial.begin(9600);
  // Setup della comunicazione seriale con il bridge interno per ricevere i comandi per ogni servo
  finestra_nord.attach(finestra_nord_pin);
  finestra_sud.attach(finestra_sud_pin);
  // Setup dei push button dedicati all'azionamento manuale delle finestre (1 button per finestra)
  pinMode(button_nord_pin, INPUT);
  pinMode(button_sud_pin, INPUT);
  // Setup posizione iniziale dei servo: chiudiamo le finestre
  finestra_nord.write(CLOSED_NORD);
  finestra_sud.write(CLOSED_SUD);
  // Setup valore iniziale dei bottoni: LOW (released)
  current_nord_button_value = LOW;
  current_sud_button_value = LOW;
  // Setup stato iniziale dei bottoni
  current_state_nord = S0;
  current_state_sud = S0;
  last_change_time = millis();
}

states get_new_state(states current_state, int pin) {
  states future_state = current_state;
  int in;
  int current_button_value = digitalRead(pin); // HIGH = button pressed, LOW = button released

  if (current_button_value == HIGH)
    in = PRESSED;
  else
    in = RELEASED;

  if (current_state == S0 && in == PRESSED) {
    future_state = S1;
  } else if (current_state == S1 && in == PRESSED) {
    future_state = S2;
  } else if (current_state == S1 && in == RELEASED) {
    future_state = S0;
  } else if (current_state == S2 && in == RELEASED) {
    future_state = S0;
  }

  return future_state;
}

void write_on_serial(char pin) {
  Serial.write(0xff);
  Serial.write(0x01); // Lunghezza payload in byte
  Serial.write(pin);
  Serial.write(0xfe);
}

void open_nord_window(int cur_position) {
  for (; cur_position <= OPEN_NORD; ++cur_position) {
    finestra_nord.write(cur_position);
    delay(10);
  }
}

void close_nord_window(int cur_position) {
  for (; cur_position >= CLOSED_NORD; --cur_position) {
    finestra_nord.write(cur_position);
    delay(10);
  }
}

void open_sud_window(int cur_position) {
  for (; cur_position >= OPEN_SUD; --cur_position) {
    finestra_sud.write(cur_position);
    delay(10);
  }
}

void close_sud_window(int cur_position) {
  for (; cur_position <= CLOSED_SUD; ++cur_position) {
    finestra_sud.write(cur_position);
    delay(10);
  }
}


void loop() {
  output_symbols out_nord;
  output_symbols out_sud;
  int pos_nord = finestra_nord.read();
  int pos_sud = finestra_sud.read();

  if (millis() - last_change_time > DEBOUNCING_TIME) {
    last_change_time = millis();
    current_state_nord = get_new_state(current_state_nord, button_nord_pin);
    current_state_sud = get_new_state(current_state_sud, button_sud_pin);

    // aggiorno gli stati della FSM
    if (current_state_nord == S1)
      out_nord = MOVE;
    else
      out_nord = NOT_MOVE;

    if (current_state_sud == S1)
      out_sud = MOVE;
    else
      out_sud = NOT_MOVE;


    if (out_nord == MOVE) {
      if (pos_nord == CLOSED_NORD) {
        write_on_serial(finestra_nord_pin); // scriviamo su seriale per comunicare al bridge cambio stato manuale: bridge imposterà un timeout
        open_nord_window(pos_nord);
      }
      else if (pos_nord == OPEN_NORD) {
        write_on_serial(finestra_nord_pin);
        close_nord_window(pos_nord);
      }
    }
    if (out_sud == MOVE) {
      if (pos_sud == CLOSED_SUD) {
        write_on_serial(finestra_sud_pin);
        open_sud_window(pos_sud);
      }
      else if (pos_sud == OPEN_SUD) {
        write_on_serial(finestra_sud_pin);
        close_sud_window(pos_sud);
      }
    }
  }

  if (Serial.available() == 2) {
    // Leggo dati dal bridge (seriale) e in base alla nuova posizione ricevuta modifico lo stato del servo motore relativo al pin ricevuto
    // Primo byte è pin del servo da azionare, secondo byte è la nuova posizione del servo
    int servo_pin = Serial.read() - '0';
    int new_pos = Serial.read() - '0';

    if (servo_pin == finestra_nord_pin) { // aziona servo della finestra nord
      if (new_pos == OPEN)
        open_nord_window(pos_nord);
      else if (new_pos == CLOSED)
        close_nord_window(pos_nord);

    } else if (servo_pin == finestra_sud_pin) { // aziona servo della finestra sud
      if (new_pos == OPEN)
        open_sud_window(pos_sud);
      else if (new_pos == CLOSED)
        close_sud_window(pos_sud);
    }
  }
}
