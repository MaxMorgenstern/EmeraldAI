#include "Arduino.h"


int motorPin1_1 = 4;
int motorPin1_2 = 5;
int motorPin1_speed = 3;

int motorPin2_1 = 7;
int motorPin2_2 = 8;
int motorPin2_speed = 6;

int motorPin3_1 = 10;
int motorPin3_2 = 11;
int motorPin3_speed = 9;

int globalSpeedInit = 255;
int reducedSpeed = globalSpeedInit * 0.09;

int encoderValue_A = 0;
int encoderValue_B = 0;
int encoder_PinA = A2;
int encoder_PinB = A3;


void setup()
{
  Serial.begin(9600);
  while (!Serial)
    ;
  Serial.println("Init");

  pinMode(motorPin1_1, OUTPUT);
  pinMode(motorPin1_2, OUTPUT);
  pinMode(motorPin1_speed, OUTPUT);

  pinMode(motorPin2_1, OUTPUT);
  pinMode(motorPin2_2, OUTPUT);
  pinMode(motorPin2_speed, OUTPUT);

  pinMode(motorPin3_1, OUTPUT);
  pinMode(motorPin3_2, OUTPUT);
  pinMode(motorPin3_speed, OUTPUT);
}


void SetMotor(int pinSpeed, int pin1, int pin2, int speed)
{
  analogWrite(pinSpeed, abs(speed));
  if (speed < 0)
  {
    analogWrite(pin1, 0);
    analogWrite(pin2, 255);
  }
  else
  {
    analogWrite(pin1, 255);
    analogWrite(pin2, 0);
  }

  if (speed == 0)
  {
    analogWrite(pin1, 0);
    analogWrite(pin2, 0);
  }
}




void loop()
{
  /*
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 0);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 0);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, 0);
  delay(2000);
  */
  int direction = 0;
  Serial.println(degrees(direction));
  Serial.println(degrees(direction+90));
  Serial.println(atan2(1, 0));
  int deg1 = 60;
  int deg2 = 180;
  int deg3 = 300;

  float vx = cos(direction) * 255;
  float vy = sin(direction) * 255;

  Serial.println(vx);
  Serial.println(vy);

  Serial.print("----------\n");

  float w3 = -vx;
  float w2 = 0.5 * vx - sqrt(3)/2 * vy;
  float w1 = 0.5 * vx + sqrt(3)/2 * vy;

  int map1 = map(abs(w1), 0, 600, 0, 255);
  int map2 = map(abs(w2), 0, 600, 0, 255);
  int map3 = map(abs(w3), 0, 600, 0, 255);

  Serial.println(w1);
  Serial.println(w2);
  Serial.println(w3);

  Serial.print("----------\n");

  Serial.println(map1);
  Serial.println(map2);
  Serial.println(map3);

/*
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, w1);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, w2);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, w3);
  delay(2500);
*/
/*
  float F1 = globalSpeedInit * cos(deg1 - direction);
  float F2 = globalSpeedInit * cos(deg2 - direction);
  float F3 = globalSpeedInit * cos(deg3 - direction);

  Serial.println(F1);
  Serial.println(F2);
  Serial.println(F3);
*/
/*
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, F1);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, F2);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, F3);
  delay(2500);
*/

  delay(100000);
}
