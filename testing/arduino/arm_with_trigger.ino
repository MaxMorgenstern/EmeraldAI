#include "Arduino.h"
#include "Servo.h"

// Servo
Servo ServoMotor_Bottom;
const uint8_t servoBotttom_Pin = 3;
uint16_t servoBottom_Pos = 90;

Servo ServoMotor_Top;
const uint8_t servoTop_Pin = 6;
uint16_t servoTop_Pos = 90;

Servo ServoMotor_Trigger;
const uint8_t servoTrigger_Pin = 9;
const uint16_t servoTrigger_Pos = 100;
const uint16_t servoTrigger_PosShoot = 135;

const uint8_t servoRotationStep = 10;


// Joystick
const uint8_t buttonX = A0;
const uint8_t buttonY = A1;
const uint8_t buttonSW = 4;


void setup()
{
    pinMode(buttonSW, INPUT_PULLUP);

    ServoMotor_Bottom.attach(servoBotttom_Pin, 400, 2600);
    ServoMotor_Bottom.write(servoBottom_Pos);

    ServoMotor_Top.attach(servoTop_Pin, 400, 2600);
    ServoMotor_Top.write(servoTop_Pos);

    ServoMotor_Trigger.attach(servoTrigger_Pin, 400, 2600);
    ServoMotor_Trigger.write(servoTrigger_Pos);
}

void loop()
{
    if(digitalRead(buttonSW) == 0)
    {
        ServoMotor_Trigger.write(servoTrigger_PosShoot);
        delay(200);
        ServoMotor_Trigger.write(servoTrigger_Pos);
        return;
    }

    servoBottom_Pos += map(analogRead(buttonX), 0, 1024, -servoRotationStep, servoRotationStep);
    servoTop_Pos += map(analogRead(buttonY), 0, 1024, -servoRotationStep, servoRotationStep);
    delay(50);

    ServoMotor_Bottom.write(servoBottom_Pos);
    ServoMotor_Top.write(servoTop_Pos);
}
