#include "Arduino.h"
#include "Adafruit_NeoPixel.h"
#include "Servo.h"
#include "NewPing.h"

// Base Date
const uint16_t initialDelay = 2500;

// Ranges and Data
const uint8_t rangeLimit_Warning1 = 60;
const uint8_t rangeLimit_Warning2 = 50;
const uint8_t rangeLimit_Warning3 = 40;
const uint8_t rangeLimit_Stop = 25;
const uint8_t motorSpeed = 255;

const uint16_t rangeLimit_RotateFor = 1000;
unsigned long rangeLimit_Timestamp = 0;
bool wheelSpinCompleted = true;


// Ultrasonic Sensor
const uint8_t trigPin = 8;
const uint8_t echoPin = 9;
const uint16_t maxDistance = 200;

NewPing sonar(trigPin, echoPin, maxDistance);

uint16_t rangeLeft;
uint16_t rangeCenter;
uint16_t rangeRight;
uint16_t lastRange;

// LED
const uint8_t ledPin = 11;
const bool ledBatterySaving = true;
Adafruit_NeoPixel LEDStrip = Adafruit_NeoPixel(26, ledPin, NEO_GRB + NEO_KHZ800);

// Motor / Wheels
const uint8_t motorPin1_1 = 4;
const uint8_t motorPin1_2 = 5;

const uint8_t motorPin2_1 = 7;
const uint8_t motorPin2_2 = 6;

const uint8_t motorEnablePin = 3;

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 10;

const uint8_t servoLimitLeft = 10;
const uint8_t servoTiltLeft = 50;
const uint8_t servoLimitRight = 170;
const uint8_t servoTiltRight = 130;
const uint8_t servoCenter = 90;

enum direction {
  LEFT,
  NONE,
  RIGHT
};
direction servoRangeDirection = NONE;

// IR obstacle detection
int obstaclePin = A1;


void setup()
{
    // Scanner
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input

    rangeLimit_Timestamp = millis();

    pinMode(motorEnablePin, OUTPUT);
    analogWrite(motorEnablePin, 255);

    // Motor
    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);

    // IR Detector
    pinMode(obstaclePin, INPUT);

    Serial.begin(9600); // Starts the serial communication

    LEDStrip.begin();
    LEDStrip.show(); // Initialize all pixels to 'off'

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin);
    ServoMotor.write(servoCenter);
    ServoMotor.detach();
}

void GetRange(int servoPos, bool rotating)
{
    long range = sonar.ping_cm();

    // fallback if return value is out of range
    if(range == 0 && rotating) { range = maxDistance; }
    if(range == 0) { range = lastRange; }
    if(range > 0  && !rotating) { lastRange = range;}

    if(servoPos == servoCenter) { rangeCenter = range; }
    if(servoPos < servoCenter) { rangeLeft = range; }
    if(servoPos > servoCenter) { rangeRight = range; }
}

bool GetObstacle()
{
    if(analogRead(obstaclePin) < 500)
    {
        return true;
    }
    return false;
}

void SetServoAngle(uint8_t angle)
{
    ServoMotor.write(angle);
    delay(20);
}


void SetMotor(int pin1, int pin2, int speed)
{
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


void ColorSet(uint32_t c)
{
    for(uint16_t i=0; i < LEDStrip.numPixels(); i++)
    {
        if(ledBatterySaving && i%8 == 0 || !ledBatterySaving)
        {
            LEDStrip.setPixelColor(i, c);
        }
    }
    LEDStrip.show();
}


void SetLightByRange(long range)
{
    uint32_t color = LEDStrip.Color(0, 255, 0);
    if(range < rangeLimit_Warning1) { color = LEDStrip.Color(127, 255, 0);}
    if(range < rangeLimit_Warning2) { color = LEDStrip.Color(255, 255, 0); }
    if(range < rangeLimit_Warning3) { color = LEDStrip.Color(255, 127, 0); }
    if(range < rangeLimit_Stop) { color = LEDStrip.Color(255, 0, 0); }

    ColorSet(color);
}

void SetLightInitState()
{
    ColorSet(LEDStrip.Color(255, 255, 255));

    SetMotor(motorPin1_1, motorPin1_2, 0);
    SetMotor(motorPin2_1, motorPin2_2, 0);
}

void SetLightErrorState()
{
    ColorSet(LEDStrip.Color(0, 0, 255));

    SetMotor(motorPin1_1, motorPin1_2, 0);
    SetMotor(motorPin2_1, motorPin2_2, 0);
}

void SetServoRangeDirection()
{
    if(rangeLeft > rangeRight)
    {
        servoRangeDirection = LEFT;
    }
    else
    {
        servoRangeDirection = RIGHT;
    }
}

void loop()
{
    uint32_t uptime = millis();
    uint16_t servoPos = ServoMotor.read();

    Serial.print(servoPos);
    Serial.print(" - ");
    Serial.println(rangeCenter);

    GetRange(servoPos, wheelSpinCompleted);

    // Wait for initial scans before performing any actions
    if(uptime < initialDelay)
    {
        SetLightInitState();
        return;
    }

    bool obstacleFound  = GetObstacle();
    if(obstacleFound)
    {
        SetLightErrorState();
    }
    else
    {
        SetLightByRange(rangeCenter);
    }

    // obstacle is further away than X cm
    // and no obstacle in front of the IR sensor
    if(!obstacleFound && wheelSpinCompleted && rangeCenter > rangeLimit_Stop)
    {
        rangeLimit_Timestamp = uptime;

        // slightly turn if side better than center
        if(rangeCenter < rangeLimit_Warning1 && rangeRight > 0 && rangeLeft > 0)
        {
            if(rangeRight > rangeLeft && rangeRight > rangeCenter )
            {
                // drive straight
                SetMotor(motorPin1_1, motorPin1_2, motorSpeed);
                SetMotor(motorPin2_1, motorPin2_2, motorSpeed/2);
            }

            if(rangeLeft > rangeRight && rangeLeft > rangeCenter )
            {
                // drive straight
                SetMotor(motorPin1_1, motorPin1_2, motorSpeed/2);
                SetMotor(motorPin2_1, motorPin2_2, motorSpeed);
            }
        }


        // drive straight
        SetMotor(motorPin1_1, motorPin1_2, motorSpeed);
        SetMotor(motorPin2_1, motorPin2_2, motorSpeed);

        return;
    }


    else
    {
        if(servoRangeDirection == NONE)
        {
            SetServoRangeDirection();
        }

        if(servoRangeDirection == LEFT)
        {
            SetMotor(motorPin1_1, motorPin1_2, -motorSpeed);
            SetMotor(motorPin2_1, motorPin2_2, motorSpeed);
        }
        else
        {
            SetMotor(motorPin1_1, motorPin1_2, motorSpeed);
            SetMotor(motorPin2_1, motorPin2_2, -motorSpeed);
        }

        wheelSpinCompleted = false;

        if(rangeCenter > rangeLimit_Warning3 && (rangeLimit_Timestamp + rangeLimit_RotateFor) <= uptime)
        {
            wheelSpinCompleted = true;
            servoRangeDirection = NONE;
        }
    }
}

