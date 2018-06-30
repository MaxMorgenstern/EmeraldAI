#include "Arduino.h"
#include "Servo.h"
#include "Wire.h"
#include "VL53L0X.h"

// Laser
VL53L0X Sensor1;
VL53L0X Sensor2;

const uint8_t Sensor1_xshut = 5;
const uint8_t Sensor2_xshut = 4;

const uint8_t Sensor1_address = 25;
const uint8_t Sensor2_address = 22;

const uint16_t minDistance = 30;
const uint16_t maxDistance = 1200;


// Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
uint8_t servoRotationAngle = 5;
const uint8_t servoRotationAngleFast = 10;
const uint8_t servoRotationAngleMedium = 5;
const uint8_t servoRotationAngleDetailed = 1;

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
    pinMode(Sensor1_xshut, OUTPUT);
    pinMode(Sensor2_xshut, OUTPUT);
    digitalWrite(Sensor1_xshut, LOW);
    digitalWrite(Sensor2_xshut, LOW);

    Wire.begin();
    Serial.begin(115200);

    pinMode(Sensor1_xshut, INPUT);
    Sensor1.init();
    Sensor1.setAddress(Sensor1_address);
    Sensor1.setTimeout(500);
    Sensor1.startContinuous();
  
    pinMode(Sensor2_xshut, INPUT);
    Sensor2.init();
    Sensor2.setAddress(Sensor2_address);
    Sensor2.setTimeout(500);
    Sensor2.startContinuous();

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 450, 2400); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
    servoRotationAngle = servoRotationAngleMedium;
}


long GetRange(int id)
{
    if(id == 1 || id == 2)
    {
        int dist = 0;
      
        if(id == 1)
        {
            dist = Sensor1.readRangeContinuousMillimeters();
        }
    
        if(id == 2)
        {
            dist = Sensor2.readRangeContinuousMillimeters();
        }
        
        if(dist < minDistance) { dist = maxDistance; }
        if(dist > maxDistance) { dist = maxDistance; }

        return dist;
    }

    return 0;
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
        servoPos += servoRotationAngle;
    }
    else
    {
        servoPos -= servoRotationAngle;
    }

    if(servoPos <= 0) { servoPos = 0; }
    if(servoPos >= 180) { servoPos = 180; }

    return servoPos;
}


void ReadDataAndSetSpeed()
{
    String data;
    if (Serial.available() > 0) {
        data = Serial.readStringUntil(';');

        if(data == "fast")
        {
            servoRotationAngle = servoRotationAngleFast;
            return;
        }

        if(data == "medium")
        {
            servoRotationAngle = servoRotationAngleMedium;
            return;
        }

        if(data == "detail")
        {
            servoRotationAngle = servoRotationAngleDetailed;
            return;
        }
    }
}

void SendData(String sensorName, int pos, int distance)
{
    Serial.print("Laser");
    Serial.print("|");
    Serial.print(sensorName);
    Serial.print("|");
    Serial.print(pos);
    Serial.print("|");
    Serial.print(distance);
    Serial.print("|");
    Serial.println(servoRotationAngle);
}


void loop()
{
    ReadDataAndSetSpeed();

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        uint8_t nextAngle = GetNextServoAngle();
        ServoMotor.write(nextAngle);
        delay(seroRotationDurationPerAngle * (abs(nextAngle - actualServoPos)));
    }

    long laserOne = GetRange(1);
    long laserTwo = GetRange(2);

    SendData("One", (servoPos), laserOne);
    SendData("Two", (servoPos+180%360), laserTwo);
}
