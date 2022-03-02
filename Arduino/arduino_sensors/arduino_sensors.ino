const int potentiometer_pin = A0;
const int photoresistor_pin = A1;
const int thermometer_pin = A2;

int previous_potentiometer_value;
int current_potentiometer_value;
int photoresistor_value;
int thermometer_value;

unsigned long lasttime;

void setup(){
  
  Serial.begin(9600);
  pinMode(potentiometer_pin, INPUT);
  pinMode(photoresistor_pin, INPUT);
  pinMode(thermometer_pin, INPUT);
  lasttime = millis();
}

void loop(){
  if (millis() - lasttime > 5000) {
    lasttime = millis();
    
    current_potentiometer_value = analogRead(potentiometer_pin);
    photoresistor_value = analogRead(photoresistor_pin);
    thermometer_value = analogRead(thermometer_pin);

    Serial.write(0xff);
    Serial.write(0x03); // Lunghezza payload in byte
    Serial.write((char)(map(current_potentiometer_value, 0, 1024, 0, 253)));  // Da 0 a 253 e non 255 perchè 254 e 255 (fe e ff) servono per l'header e il footer del pacchetto
    Serial.write((char)(map(photoresistor_value, 0, 1024, 0, 253)));
    Serial.write((char)(map(thermometer_value, 0, 1024, 0, 253)));
    Serial.write(0xfe);
  }
}
