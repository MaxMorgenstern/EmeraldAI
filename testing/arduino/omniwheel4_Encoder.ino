#include "Arduino.h"

int motorPin1_1 = 4;
int motorPin1_2 = 5;
int motorPin1_speed = 3;
int motorPin1_A = A7;

int motorPin2_1 = 7;
int motorPin2_2 = 8;
int motorPin2_speed = 6;
int motorPin2_A = A6;

int motorPin3_1 = 10;
int motorPin3_2 = 11;
int motorPin3_speed = 9;
int motorPin3_A = A5;

int globalSpeedInit = 255;
int reducedSpeed = globalSpeedInit * 0.09;

void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ;
    Serial.println("Init");

    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);
    pinMode(motorPin1_speed, OUTPUT);
    pinMode(motorPin1_A, INPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);
    pinMode(motorPin2_speed, OUTPUT);
    pinMode(motorPin2_A, INPUT);

    pinMode(motorPin3_1, OUTPUT);
    pinMode(motorPin3_2, OUTPUT);
    pinMode(motorPin3_speed, OUTPUT);
    pinMode(motorPin3_A, INPUT);

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

int motor1_RPMCount = 0;
int motor1_State = 0;

int motor2_RPMCount = 0;
int motor2_State = 0;

int motor3_RPMCount = 0;
int motor3_State = 0;


// 1 Rotation == 80 Gearbox Ratio ==
//      4 CPR (counts per revolution) * 80 == 320 Counts per Rotation
int pulsesPerRotation = 320

void loop()
{

    int state = (analogRead(motorPin1_A) < 500) ? 0 : 1;
    if(state != motor1_State)
    {
        motor1_RPMCount++;
        motor1_State = state;
    }

    int state = (analogRead(motorPin2_A) < 500) ? 0 : 1;
    if(state != motor2_State)
    {
        motor2_RPMCount++;
        motor2_State = state;
    }

    int state = (analogRead(motorPin3_A) < 500) ? 0 : 1;
    if(state != motor3_State)
    {
        motor3_RPMCount++;
        motor3_State = state;
    }

}
