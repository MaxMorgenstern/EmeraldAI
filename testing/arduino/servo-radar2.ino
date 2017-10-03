#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"

// Base Date
const uint16_t initialDelay = 2500;

// Ultrasonic Sensor
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;
const uint16_t maxDistance = 300;

NewPing sonar(trigPin, echoPin, maxDistance);

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
    Serial.begin(9600); // Starts the serial communication

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin);
    ServoMotor.write(servoPos);
}


void CalculateAverageRange()
{
    long range = sonar.ping_cm();

    Serial.print(servoPos);
    Serial.print(" - ");
    Serial.println(range);

    if(range == 0)
    {
        //delay(5000);
    }

    long *rangeData_Current;

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
    delay(20);

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
    if(servoPos <= 10)
    {
        servoMovement = right;
        servoPos = 10;
    }

    if(servoPos >= 170)
    {
        servoMovement = left;
        servoPos = 170;
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
    //Serial.println(average_Center);
}


