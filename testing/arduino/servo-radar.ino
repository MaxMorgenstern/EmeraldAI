#include "Arduino.h"
#include "Servo.h"

// Base Date
const uint8_t initialDelay = 2500;

// Ultrasonic Sensor
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;

long rangeData_Left[15];
long average_Left;
long rangeData_Center[10];
long average_Center;
long rangeData_Right[15];
long average_Right;
uint8_t rangeDataIndex = 0;

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
const uint8_t servoRotationAngel = 10;

enum direction {
  left,
  center,
  right
};

uint8_t servoPos = 90;
direction servoMovement = right;
direction servoLocation = center;


void setup()
{
    // Scanner
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input

    Serial.begin(9600); // Starts the serial communication

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin);
    ServoMotor.write(servoPos);
}


long MicrosecondsToCentimeters(long microseconds)
{
    return microseconds / 29 / 2;
}


// Use library to minimize delay
long GetUltrasoundRange()
{
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);

    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    long duration = pulseIn(echoPin, HIGH);

    // convert the time into a distance
    return MicrosecondsToCentimeters(duration);
}


void CalculateAverageRange()
{
    long range = GetUltrasoundRange();
    long **rangeData_Current;

    // get current meassurement and add to array
    if(servoLocation == left)
    {
        rangeData_Left[rangeDataIndex++] = range;
        rangeData_Current = rangeData_Left;
    }

    if(servoLocation == center)
    {
        rangeData_Center[rangeDataIndex++] = range;
        rangeData_Current = rangeData_Center;
    }

    if(servoLocation == right)
    {
        rangeData_Right[rangeDataIndex++] = range;
        rangeData_Current = rangeData_Right;
    }

    direction servoLocationLast = servoLocation;
    direction servoMovementLast = servoMovement;

    // Get the next Angle and Move the Servo
    ServoMotor.write(GetNextServoAngle());

    // if the new servo location is different from the one before calculate an anverage
    if(servoLocation != servoLocationLast || servoMovement != servoMovementLast)
    {
        long summedUp = 0;
        for (int i = 0; i < rangeDataIndex; i++)
        {
            summedUp += rangeData_Current[i];
            rangeData_Current[i] = 0;
        }

        long average = summedUp/rangeDataIndex;
        if(servoLocationLast == left) { average_Left = average; }
        if(servoLocationLast == center) { average_Center = average; }
        if(servoLocationLast == right) { average_Right = average; }

        rangeDataIndex = 0;
    }
}


uint8_t GetNextServoAngle()
{
    // 0 - 80 / 80 - 100 / 100 - 180
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


    if(servoPos < 80)
    {
        servoLocation = left;
    }

    if(servoPos >= 80 && servoPos <= 100)
    {
        servoLocation = center;
    }

    if(servoPos > 100)
    {
        servoLocation = right;
    }

    return servoPos;
}


void loop()
{

    CalculateAverageRange();

    // Wait for initial scans before performing any actions
    if(millis() < initialDelay)
    {
        return;
    }

    long range = average_Center;
}


