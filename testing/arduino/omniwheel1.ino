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

/*
  void countA() {

  encoderValue_A++;
  }

  void countB() {

  encoderValue_B++;
  }
*/



void SetMotor(int pinSpeed, int pin1, int pin2, int speed, bool CW)
{
  analogWrite(pinSpeed, speed);
  if (!CW)
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

  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, globalSpeedInit, true);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, globalSpeedInit, true);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, globalSpeedInit, true);
  delay(2500);
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, globalSpeedInit, false);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, globalSpeedInit, false);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, globalSpeedInit, false);
  delay(2500);


  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, globalSpeedInit, true);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, globalSpeedInit, false);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, 0, true);
  delay(2500);
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, globalSpeedInit, false);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, globalSpeedInit, true);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, 0, true);
  delay(2500);


  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, reducedSpeed, true);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, reducedSpeed, true);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, globalSpeedInit, false);
  delay(2500);
  SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, reducedSpeed, false);
  SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, reducedSpeed, false);
  SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, globalSpeedInit, true);
  delay(2500);


}
