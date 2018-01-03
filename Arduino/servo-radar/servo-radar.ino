#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"

// Ultrasonic Sensor
const uint16_t maxDistance = 250;

// Ultrasonic Sensor #1
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;
const char sonar1Name[] = "Front";


NewPing sonar1(trigPin, echoPin, maxDistance);

// Ultrasonic Sensor #2
const uint8_t trigPin2 = 11;
const uint8_t echoPin2 = 12;
const char sonar2Name[] = "Back";

NewPing sonar2(trigPin2, echoPin2, maxDistance);

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
uint8_t servoRotationAngel = 5;
const uint8_t servoRotationAngelFast = 10;
const uint8_t servoRotationAngelMedium = 5;
const uint8_t servoRotationAngelDetailed = 1;

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
    Serial.begin(115200);

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2600); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
    servoRotationAngel = servoRotationAngelMedium;
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


void ReadDataAndSetSpeed()
{
    String data;
    if (Serial.available() > 0) {
        data = Serial.readStringUntil(';');

        if(data = "fast")
        {
            servoRotationAngel = servoRotationAngelFast;
            return;
        }
        
        if(data = "medium")
        {
            servoRotationAngel = servoRotationAngelMedium;
            return;
        }

        if(data = "detail")
        {
            servoRotationAngel = servoRotationAngelDetailed;
            return;
        }
    }
}


void loop()
{
    ReadDataAndSetSpeed();
    
    long rangeFront = GetRange(1);
    long rangeBack = GetRange(2);

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        uint8_t nextAngle = GetNextServoAngle();
        ServoMotor.write(nextAngle);
        delay(seroRotationDurationPerAngle * (abs(nextAngle - actualServoPos)));
    }

    if(rangeFront > 0)
    {
        Serial.print("Ultrasonic");
        Serial.print("|");
        Serial.print(sonar1Name);
        Serial.print("|");
        Serial.print(servoPos);
        Serial.print("|");
        Serial.println(rangeFront);
    }

    if(rangeBack > 0)
    {
        Serial.print("Ultrasonic");
        Serial.print("|");
        Serial.print(sonar2Name);
        Serial.print("|");
        Serial.print((servoPos+180%360));
        Serial.print("|");
        Serial.println(rangeBack);
    }

}

