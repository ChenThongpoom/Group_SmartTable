const int pingPin = 13;
int inPin = 12;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  long duration, cm;

  pinMode(pingPin, OUTPUT);

  digitalWrite(pingPin, LOW);
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);
  delayMicroseconds(5);
  digitalWrite(pingPin, LOW);
  pinMode(inPin, INPUT);
  duration = pulseIn(inPin, HIGH);

  cm = microsecondsToCentimeters(duration);

  Serial.print(cm);
  Serial.print("cm");
  Serial.println();
  delay(100);
  
}


long microsecondsToCentimeters(long microseconds){
  return microseconds / 29 / 2;
  // The speed of sound is 340 m/s or 29 microseconds per centimeters.
  // The ping travels out and back, so to find the distance of the
  // object we take half of the distance travelled
}
