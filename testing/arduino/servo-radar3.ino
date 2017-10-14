#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"

// Ultrasonic Sensor
const uint16_t maxDistance = 300;

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
const uint8_t servoRotationAngel = 10;
const uint8_t servoRotationAngelDetailed = 1;

enum direction {
  left,
  center,
  right
};

uint8_t servoPos = 90;
direction servoMovement = right;


void setup()
{
    Serial.begin(115200); // Starts the serial communication

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2600);
    ServoMotor.write(servoPos);
}


long GetRange1()
{
    long range = sonar1.ping_cm();

    // fallback if return value is out of range
    if(range == 0) { range = maxDistance; }

    return range;
}

long GetRange2()
{
    long range = sonar2.ping_cm();

    // fallback if return value is out of range
    if(range == 0) { range = maxDistance; }

    return range;
}


uint8_t GetNextServoAngle(bool detailed)
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

    uint8_t angle = servoRotationAngel;
    if(detailed)
    {
        angle = servoRotationAngelDetailed;
    }

    if(servoMovement == right)
    {
        servoPos += angle;
    }
    else
    {
        servoPos -= angle;
    }

    return servoPos;
}


void loop()
{
    long range1 = GetRange1();
    long range2 = GetRange2();
    uint8_t actualServoPos = ServoMotor.read();

    if(servoPos == actualServoPos)
    {
        // Change to true for detailed scan
        ServoMotor.write(GetNextServoAngle(false));
        delay(10);
    }

    Serial.print("#1: ");
    Serial.print(actualServoPos);
    Serial.print(" - ");
    Serial.println(range1);

    Serial.print("#2: ");
    Serial.print(actualServoPos+180);
    Serial.print(" - ");
    Serial.println(range2);
}
