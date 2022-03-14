const int potentiometer_pin = A0;
const int photoresistor_pin = A1;
const int thermometer_pin = A2;
const int button_pin_sud = 2; // azionamento manuale scuri finestra sud
const int button_pin_nord = 3; // azionamento manuale scuri finestra nord

int potentiometer_value;
int photoresistor_value;
int thermometer_value;
bool button_value_sud;
bool button_value_nord;

unsigned long lasttime;

void setup(){
  
  Serial.begin(9600);
  pinMode(potentiometer_pin, INPUT);
  pinMode(photoresistor_pin, INPUT);
  pinMode(thermometer_pin, INPUT);
  pinMode(button_pin_sud, INPUT);
  pinMode(button_pin_nord, INPUT);
  lasttime = millis();
}

void loop(){
  if (millis() - lasttime > 5000) {
    lasttime = millis();
    
    potentiometer_value = analogRead(potentiometer_pin); // controllare la velocità del vento: deltaValue ogni 5 secondi -> possibile deltaValue = 25
    photoresistor_value = analogRead(photoresistor_pin); // soglia = 100 (selezionare uint8 in realterm)
    thermometer_value = analogRead(thermometer_pin);
    button_value_sud = digitalRead(button_pin_sud); // HIGH = button pressed (--> cambia stato della finestra sud), LOW = button released
    button_value_nord = digitalRead(button_pin_nord); // HIGH = button pressed (--> cambia stato della finestra nord), LOW = button released
    
    Serial.write(0xff);
    Serial.write(0x04); // Lunghezza payload in byte
    Serial.write((char)(map(potentiometer_value, 0, 1024, 0, 253)));  // Da 0 a 253 e non 255 perchè 254 e 255 (fe e ff) servono per l'header e il footer del pacchetto
    Serial.write((char)(map(photoresistor_value, 0, 1024, 0, 253)));
    Serial.write((char)(map(button_value_sud, 0, 1, 0, 253)));
    Serial.write((char)(map(button_value_nord, 0, 1, 0, 253)));
    Serial.write(0xfe);
  }
}
