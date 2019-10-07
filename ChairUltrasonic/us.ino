
#include <ESP8266WiFi.h>


#define D8 15
#define first_pingPin D8
#define D7 13
#define first_inPin D7
#define D5 14
#define second_pingPin D5
#define D6 12
#define second_inPin D6


//const int first_pingPin = 13, second_pingPin = 11;
long duration, cm;
//int first_inPin = 12, second_inPin = 10;
const char *ssid = "CIE";
const char *password = "despacito2";



void activate(int,int);

void setup() {
  
  Serial.begin(9600);
  pinMode(first_pingPin, OUTPUT);
//  pinMode(second_pingPin, OUTPUT);
  pinMode(first_inPin, INPUT);
//  pinMode(second_inPin, INPUT);

  Serial.println("Starting...");
  WiFi.begin(ssid,password);
  while( WiFi.status() != WL_CONNECTED){
    delay(250);
    Serial.print(".");
  }

  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

}
void loop()
{
  
  long first_distance, second_distance; 
  
  activate(first_pingPin,first_inPin);
  first_distance = cm;
  activate(second_pingPin,second_inPin);
  second_distance = cm;

  if (first_distance >=100 or second_distance >= 100)
  {
    Serial.println("Over 100 cm far!");
  }
  else if(abs(first_distance - second_distance)>10){
     Serial.println("please sit properly!"); 
    }
  else{
     Serial.println("correct");
    }
}



void activate(int trig,int echo){

  
  digitalWrite(trig, LOW);
  delayMicroseconds(5);
  digitalWrite(trig, HIGH);
  delayMicroseconds(20);
  digitalWrite(trig,LOW);

  duration = pulseIn(echo,HIGH);
  cm = (duration / 2) / 29.1;
  
}
