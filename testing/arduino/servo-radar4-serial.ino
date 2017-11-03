#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"

// Ultrasonic Sensor
const uint16_t maxDistance = 250;

// Ultrasonic Sensor #1
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;

NewPing sonar1(trigPin, echoPin, maxDistance);

// Ultrasonic Sensor #2
const uint8_t trigPin2 = 11;
const uint8_t echoPin2 = 12;

NewPing sonar2(trigPin2, echoPin2, maxDistance);

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
const uint8_t servoRotationAngel = 5;
const uint8_t seroRotationDurationPerAngle = 2;

enum direction {
    left,
    center,
    right
};

uint8_t servoPos = 90;
direction servoMovement = right;

// ------------------------------
//            SETUP
// ------------------------------

void setup()
{
    Serial.begin(230400);

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2350); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
}


long GetRange(int id)
{
    long range = 0;
    if(id == 1)
    {
        range = sonar1.ping_cm();
    }

    if(id == 2)
    {
        range = sonar2.ping_cm();
    }

    return range;
}


uint8_t GetNextServoAngle()
{
    if(servoPos <= 0)
    {
        servoMovement = right;
        servoPos = 0;
    }

    if(servoPos >= 180)
    {
        servoMovement = left;
        servoPos = 180;
    }


    if(servoMovement == right)
    {
        servoPos += servoRotationAngel;
    }
    else
    {
        servoPos -= servoRotationAngel;
    }

    return servoPos;
}


void loop()
{
    long rangeFront = GetRange(1);
    long rangeBack = GetRange(2);

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        uint8_t nextAngle = GetNextServoAngle();
        ServoMotor.write();
        delay(seroRotationDurationPerAngle * (abs(nextAngle - actualServoPos)));
    }

    if(rangeFront > 0)
    {
        Serial.print("Servo_Front");
        Serial.print("|");
        Serial.print(servoPos);
        Serial.print("|");
        Serial.println(rangeFront);
    }

    if(rangeBack > 0)
    {
        Serial.print("Servo_Back");
        Serial.print("|");
        Serial.print((servoPos+180%360);
        Serial.print("|");
        Serial.println(rangeBack);
    }

}
