#include "Arduino.h"
#include "Servo.h"

// Servo
Servo ServoMotor_Bottom;
const uint8_t servoPin_Bottom = 3;

Servo ServoMotor_Top;
const uint8_t servoPin_Top = 6;

const uint8_t servoRotationAngel = 10;


// Joystick
const uint8_t buttonX = A0;
const uint8_t buttonY = A1;
const uint8_t buttonSW = 4;


void setup()
{
    Serial.begin(9600); // Starts the serial communication

    pinMode(buttonSW, INPUT_PULLUP);

    pinMode(A5, OUTPUT);
    pinMode(buttonSW, OUTPUT);

    ServoMotor_Bottom.attach(servoPin_Bottom, 400, 2600);
    ServoMotor_Bottom.write(90);

    ServoMotor_Top.attach(servoPin_Top, 400, 2600);
    ServoMotor_Top.write(90);
}



void loop()
{
    ServoMotor_Bottom.write(map(analogRead(buttonX), 0, 1024, 0, 180));

    ServoMotor_Top.write(map(analogRead(buttonY), 0, 1024, 0, 180));


    analogWrite(A5, 255);
    if(digitalRead(buttonSW) == 0)
    {
        analogWrite(A5, 0);
    }
}
