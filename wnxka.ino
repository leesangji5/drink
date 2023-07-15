int pin1 = 7;
int pin2 = 8;
int pin3 = 9;
int st = 0;
int dt = 2000;

void setup() {
  Serial.begin(9600);
  pinMode(pin1, INPUT);
  pinMode(pin2, INPUT);
  pinMode(pin3, INPUT);
  st = millis();
}

void loop() {
  if (digitalRead(pin1) == 1 && millis()-st > dt){
    Serial.println(1);
    st = millis();
    dt = 3000;
  }
  else if (digitalRead(pin2) == 1 && millis()-st > dt){
    Serial.println(2);
    st = millis();
    dt = 9000;
  }
  else if (digitalRead(pin3) == 1 && millis()-st > dt){
    Serial.println(3);
    st = millis();
    dt = 9000;
  }
}
