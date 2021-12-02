const int potentiometer_pin = A0;
const int photoresistor_pin = A1;
const int thermometer_pin = A2;

int previous_potentiometer_value;
int current_potentiometer_value;
int previous_photoresistor_value;
int current_photoresistor_value;
int thermometer_value;

void setup(){
  Serial.begin(9600);
  pinMode(potentiometer_pin, INPUT);
  pinMode(photoresistor_pin, INPUT);
  previous_potentiometer_value = analogRead(potentiometer_pin);
  previous_photoresistor_value = analogRead(photoresistor_pin);
}

void loop(){
  current_potentiometer_value = analogRead(potentiometer_pin);
  current_photoresistor_value = analogRead(photoresistor_pin);
  thermometer_value = analogRead(thermometer_pin);
  Serial.println(current_potentiometer_value);
  Serial.println(current_photoresistor_value);
  Serial.println(thermometer_value);
}
