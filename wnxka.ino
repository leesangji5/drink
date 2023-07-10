int pin1 = 7;
int pin2 = 8;
int pin3 = 9;
int pin4 = 10;
int pin5 = 11;
int pin6 = 12;
int st = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
  pinMode(pin3, INPUT);
  pinMode(pin4, INPUT);
  pinMode(pin5, INPUT);
  pinMode(pin6, INPUT);
  st = millis();
}

void loop() {
  if (digitalRead(pin1) == 1 && millis()-st > 1000){
    Serial.println(1);
    st = millis();
  }
  else if (digitalRead(pin2) == 2 && millis()-st > 1000){
    Serial.println(2);
    st = millis();
  }
  else if (digitalRead(pin3) == 3 && millis()-st > 1000){
    Serial.println(3);
    st = millis();
  }
  else if (digitalRead(pin4) == 4 && millis()-st > 1000){
    Serial.println(4);
    st = millis();
  }
  else if (digitalRead(pin5) == 5 && millis()-st > 1000){
    Serial.println(5);
    st = millis();
  }
  else if (digitalRead(pin6) == 6 && millis()-st > 1000){
    Serial.println(6);
    st = millis();
  }
}
