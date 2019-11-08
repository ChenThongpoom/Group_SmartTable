#include <stdio.h>
#include <math.h> 

const int pingPin = 13;
const int forward = 7, forward2 = 5;
const int backward =6, backward2 = 4;
int inPin = 12;
int sum, ans;
long duration, cm;

void setup() {
Serial.begin(9600);
pinMode(forward, OUTPUT);
pinMode(forward2, OUTPUT);
pinMode(backward, OUTPUT);
pinMode(backward2, OUTPUT);
}

void loop()
{
  if (Serial.read() == 'a'){
    measure();
  }
  else if(Serial.read() == 'u'){
    linearUp();
  }
  else if (Serial.read() == 'd'){
    linearDown();
  }
  else if(Serial.read() == 'q'){
    linearStop();
  }


}


void linearUp(){
  digitalWrite(forward,HIGH);
  digitalWrite(forward2,HIGH);
  digitalWrite(backward,LOW);
  digitalWrite(backward2,LOW);
  
}


void linearDown(){
  digitalWrite(forward,LOW);
  digitalWrite(forward2,LOW);
  digitalWrite(backward,HIGH);
  digitalWrite(backward2,HIGH);
  
}


void linearStop(){
  digitalWrite(forward,LOW);
  digitalWrite(forward2,LOW);
  digitalWrite(backward,LOW);
  digitalWrite(backward2,LOW);
  
}


void measure(){

  
  pinMode(pingPin, OUTPUT);


digitalWrite(pingPin, LOW);
delayMicroseconds(2);
digitalWrite(pingPin, HIGH);
delayMicroseconds(5);
digitalWrite(pingPin, LOW);
pinMode(inPin, INPUT);
duration = pulseIn(inPin, HIGH);
cm = microsecondsToCentimeters(duration);
Serial.println(cm);

//
//if (cm > 40 and cm < 70)
//{
////  Serial.write("keep");
////  Serial.print(cm);
//  ans = calculate();
//  Serial.println(ans);
//}
//else
//{
//  Serial.println("stop");
////  Serial.print(cm);
//}
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
