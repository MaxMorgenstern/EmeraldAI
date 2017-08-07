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


float toDegrees(float angle)
{
    return angle / 360 * 2 * 3.14159267;
}

float mapper(float value)
{
    return value * globalSpeedInit;
}

int direction = 90;
void loop()
{

    int deg1 = 150;
    int deg2 = 30;
    int deg3 = 270;

    float F1 = -cos(toDegrees(deg1 - direction));
    float F2 = -cos(toDegrees(deg2 - direction));
    float F3 = -cos(toDegrees(deg3 - direction));

    Serial.println("-----");
    Serial.println(direction);
    Serial.println(mapper(F1));
    Serial.println(mapper(F2));
    Serial.println(mapper(F3));

    //direction++;
    if(direction > 359)
    {
        direction = 0;
    }

    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, mapper(F1));
    SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, mapper(F2));
    SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, mapper(F3));
    delay(10);
}
