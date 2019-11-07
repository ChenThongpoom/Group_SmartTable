#include <stdio.h>
#include <math.h> 

const int pingPin = 13;
int inPin = 12;
int sum, ans;
long duration, cm;

void setup() {
Serial.begin(9600);
}

void loop()
{


pinMode(pingPin, OUTPUT);


digitalWrite(pingPin, LOW);
delayMicroseconds(2);
digitalWrite(pingPin, HIGH);
delayMicroseconds(5);
digitalWrite(pingPin, LOW);
pinMode(inPin, INPUT);
duration = pulseIn(inPin, HIGH);
cm = microsecondsToCentimeters(duration);


if (cm > 40 and cm < 70)
{
  Serial.println("keep detecting");
//  Serial.print(cm);
  ans = calculate();
  Serial.println(ans);
}
else
{
  Serial.println("stop eye detection!");
//  Serial.print(cm);
}
  delay(500);
}

   
int calculate() {
  
  sum = (sin(20)/cos(20))*cm;
  
  printf("Range = %lf\n", cm);
  return (sum);
}

long microsecondsToCentimeters(long microseconds)
{
// The speed of sound is 340 m/s or 29 microseconds per centimeter.
// The ping travels out and back, so to find the distance of the
// object we take half of the distance travelled.
return microseconds / 29 / 2;
}
