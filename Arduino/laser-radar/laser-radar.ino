#include "Arduino.h"
#include "Servo.h"
#include "Wire.h"
#include "VL53L0X.h"

// Laser
#define XSHUT_pin4 8
#define XSHUT_pin3 7
#define XSHUT_pin2 6
#define XSHUT_pin1 5

//ADDRESS_DEFAULT 0b0101001 or 41
//#define Sensor1_newAddress 41 not required address change
#define Sensor2_newAddress 42
#define Sensor3_newAddress 43
#define Sensor4_newAddress 44

VL53L0X Sensor1;
VL53L0X Sensor2;
VL53L0X Sensor3;
VL53L0X Sensor4;


// Servo
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
    pinMode(XSHUT_pin1, OUTPUT);
    pinMode(XSHUT_pin2, OUTPUT);
    pinMode(XSHUT_pin3, OUTPUT);
    pinMode(XSHUT_pin4, OUTPUT);

    Serial.begin(115200);

    Wire.begin();

    Sensor4.setAddress(Sensor4_newAddress);
    pinMode(XSHUT_pin3, INPUT);
    delay(10);

    Sensor3.setAddress(Sensor3_newAddress);
    pinMode(XSHUT_pin2, INPUT);
    delay(10);

    Sensor2.setAddress(Sensor2_newAddress);
    pinMode(XSHUT_pin1, INPUT);
    delay(10);

    Sensor1.init();
    Sensor2.init();
    Sensor3.init();
    Sensor4.init();

    Sensor1.setTimeout(500);
    Sensor2.setTimeout(500);
    Sensor3.setTimeout(500);
    Sensor4.setTimeout(500);

    Sensor1.startContinuous();
    Sensor2.startContinuous();
    Sensor3.startContinuous();
    Sensor4.startContinuous();

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 450, 2400); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
    servoRotationAngel = servoRotationAngelMedium;
}


long GetRange(int id)
{
    if(id == 1)
    {
        return Sensor1.readRangeContinuousMillimeters();
    }

    if(id == 2)
    {
        return Sensor2.readRangeContinuousMillimeters();
    }

    if(id == 2)
    {
        return Sensor3.readRangeContinuousMillimeters();
    }

    if(id == 2)
    {
        return Sensor4.readRangeContinuousMillimeters();
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
        servoPos += servoRotationAngel;
    }
    else
    {
        servoPos -= servoRotationAngel;
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
            servoRotationAngel = servoRotationAngelFast;
            averageScanAmount = averageScanAmountFast;
            return;
        }

        if(data == "medium")
        {
            servoRotationAngel = servoRotationAngelMedium;
            averageScanAmount = averageScanAmountMedium;
            return;
        }

        if(data == "detail")
        {
            servoRotationAngel = servoRotationAngelDetailed;
            averageScanAmount = averageScanAmountDetailed;
            return;
        }
    }
}

void SendData(name, position, distance)
{
    Serial.print("Laser");
    Serial.print("|");
    Serial.print(name);
    Serial.print("|");
    Serial.print(position);
    Serial.print("|");
    Serial.println(distance);
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
    long laserThree = GetRange(3);
    long laserFrour = GetRange(4);

    SendData("One", servoPos, laserOne);
    SendData("Two", (servoPos+90%360), laserTwo);
    SendData("Three", (servoPos+180%360), laserThree);
    SendData("Four", (servoPos+270%360), laserFour);
}

