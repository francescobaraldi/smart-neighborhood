const int potentiometer_pin = A0;
const int photoresistor_pin = A1;
const int thermometer_pin = A2;

int potentiometer_value;
int photoresistor_value;
int thermometer_value;
float thermometer_degrees;

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
    
    potentiometer_value = analogRead(potentiometer_pin); // soglia = 128
    photoresistor_value = analogRead(photoresistor_pin); // soglia = 100 (selezionare uint8 in realterm)
    thermometer_value = analogRead(thermometer_pin);
    therm<ometer_degrees = ((thermometer_value / 1024) * 5 - 0.5) * 100;

    Serial.write(0xff);
    Serial.write(0x03); // Lunghezza payload in byte
    Serial.write((char)(map(potentiometer_value, 0, 1024, 0, 253)));  // Da 0 a 253 e non 255 perchè 254 e 255 (fe e ff) servono per l'header e il footer del pacchetto
    Serial.write((char)(map(photoresistor_value, 0, 1024, 0, 253)));
    Serial.write(thermometer_degrees);
    Serial.write(0xfe);
  }
}
