#include "Arduino.h"
#include "Adafruit_NeoPixel.h"
#include "Servo.h"
#include "NewPing.h"

// Base Date
const uint16_t initialDelay = 2500;

// Ranges and Data
const uint8_t rangeLimit_Warning1 = 70;
const uint8_t rangeLimit_Warning2 = 50;
const uint8_t rangeLimit_Stop = 40;
const uint8_t motorSpeed = 180; // max: 255

const uint16_t rangeLimit_RotateFor = 500;
unsigned long rangeLimit_Timestamp = 0;
bool wheelSpinCompleted = true;


// Ultrasonic Sensor
const uint8_t trigPin = 9;
const uint8_t echoPin = 8;
const uint16_t maxDistance = 200;

NewPing sonar(trigPin, echoPin, maxDistance);

uint16_t rangeLeft;
uint16_t rangeCenter;
uint16_t rangeRight;
uint16_t lastRangeLeft;
uint16_t lastRangeCenter;
uint16_t lastRangeRight;

// LED
const uint8_t ledPin = 11;
const bool ledBatterySaving = true;
Adafruit_NeoPixel LEDStrip = Adafruit_NeoPixel(24, ledPin, NEO_GRB + NEO_KHZ800);

// Motor / Wheels
const uint8_t motorPin1_1 = A3;
const uint8_t motorPin1_2 = A2;
const uint8_t motorEnablePin1 = 5;

const uint8_t motorPin2_1 = A5;
const uint8_t motorPin2_2 = A4;
const uint8_t motorEnablePin2 = 6;

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 10;

const uint8_t servoLimitLeft = 170;
const uint8_t servoTiltLeft = 130;
const uint8_t servoLimitRight = 10;
const uint8_t servoTiltRight = 50;
const uint8_t servoCenter = 90;
const uint8_t seroRotationDurationPerAngle = 2;

enum direction {
  LEFT,
  NONE,
  RIGHT
};
direction servoRangeDirection = NONE;
uint32_t servoLastScanTimestamp = 0;

direction servoLastScan = NONE;

// IR obstacle detection
int obstaclePin = A7;


void setup()
{
    Serial.begin(115200);
    // Scanner
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input

    rangeLimit_Timestamp = millis();

    pinMode(motorEnablePin1, OUTPUT);
    analogWrite(motorEnablePin1, 255);

    pinMode(motorEnablePin2, OUTPUT);
    analogWrite(motorEnablePin2, 255);

    // Motor
    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);

    // IR Detector
    pinMode(obstaclePin, INPUT);

    LEDStrip.begin();
    LEDStrip.show(); // Initialize all pixels to 'off'

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2350);
    ServoMotor.write(servoCenter);
}

void GetRange(int servoPos, bool rotating)
{
    long range = sonar.ping_cm();

    // fallback if return value is out of range
    if(range == 0 && rotating) { range = maxDistance; }
    if(range > maxDistance) { range = maxDistance; }

    
    //if(range == 0) { range = lastRange; }
    //if(range > 0  && !rotating) { lastRange = range;}

    long avgRange;

    if(servoPos == servoCenter) 
    {
        if(range == 0) { range = lastRangeCenter; }
        avgRange = (range + lastRangeCenter) / 2;
        lastRangeCenter = range;

        rangeCenter = avgRange; 
    }
    if(servoPos > servoCenter) 
    { 
        if(range == 0) { range = lastRangeLeft; }
        avgRange = (range + lastRangeLeft) / 2;
        lastRangeLeft = range;

        rangeLeft = avgRange; 
    }
    if(servoPos < servoCenter) 
    { 
        if(range == 0) { range = lastRangeRight; }
        avgRange = (range + lastRangeRight) / 2;
        lastRangeRight = range;
        
        rangeRight = avgRange; 
    }

    Serial.print(range);
    Serial.print(" - ");
    Serial.print(avgRange);
    Serial.print(" - ");
    Serial.println(servoPos);
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
    ServoMotor.write(angle);;
}


void SetMotor(int id, int speed)
{
    if(id == 1)
    {
        SetMotorWorker(motorPin1_1, motorPin1_2, motorEnablePin1, speed);
    }

    if(id == 2)
    {
        SetMotorWorker(motorPin2_1, motorPin2_2, motorEnablePin2, speed);
    }
}

void SetMotorWorker(int pin1, int pin2, int enablePin, int speed)
{
    analogWrite(enablePin, abs(speed));

    if (speed < 0)
    {
        analogWrite(pin1, 0);
        analogWrite(pin2, 255);
    }

    if (speed > 0)
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
    if(range < rangeLimit_Warning2) { color = LEDStrip.Color(255, 127, 0); }
    if(range < rangeLimit_Stop) { color = LEDStrip.Color(255, 0, 0); }

    ColorSet(color);
}

void SetLightInitState()
{
    ColorSet(LEDStrip.Color(255, 255, 255));

    SetMotor(1, 0);
    SetMotor(2, 0);
}

void SetLightErrorState()
{
    ColorSet(LEDStrip.Color(0, 0, 255));
}


void SetServo(uint32_t uptime, uint8_t servoPos)
{
    uint32_t interval = 1000;
    uint32_t returnInterval = 300;
    
    if(uptime < interval+1)
    {
        return;
    }

    if(servoLastScanTimestamp < uptime - interval)
    {
        servoLastScanTimestamp = uptime;

        if(servoLastScan == RIGHT)
        {
            SetServoAngle(servoTiltLeft);
            delay(seroRotationDurationPerAngle * (abs(servoTiltLeft - servoPos)));
            servoLastScan = LEFT;
        }
        else
        {
            SetServoAngle(servoTiltRight);
            delay(seroRotationDurationPerAngle * (abs(servoTiltRight - servoPos)));
            servoLastScan = RIGHT;
        }

        return;
    }

    if(servoLastScanTimestamp < uptime - returnInterval)
    {
        SetServoAngle(servoCenter);
        delay(seroRotationDurationPerAngle * (abs(servoCenter - servoPos)));
    }
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
    uint8_t servoPos = ServoMotor.read();

    GetRange(servoPos, wheelSpinCompleted);

    SetServo(uptime, servoPos);

    // Wait for initial scans before performing any actions
    if(uptime < initialDelay)
    {
        SetLightInitState();
        delay(20);
        return;
    }

    bool obstacleFound = GetObstacle();
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
                // drive right
                SetMotor(1, motorSpeed);
                SetMotor(2, motorSpeed*2/3);
            }

            if(rangeLeft > rangeRight && rangeLeft > rangeCenter )
            {
                // drive left
                SetMotor(1, motorSpeed*2/3);
                SetMotor(2, motorSpeed);
            }
        }

        // drive straight
        SetMotor(1, motorSpeed);
        SetMotor(2, motorSpeed);
    }
    else
    {
        if(servoRangeDirection == NONE)
        {
            SetServoRangeDirection();
        }

        if(servoRangeDirection == LEFT)
        {
            SetMotor(1, -motorSpeed);
            SetMotor(2, motorSpeed);
        }
        else
        {
            SetMotor(1, motorSpeed);
            SetMotor(2, -motorSpeed);
        }

        wheelSpinCompleted = false;

        // TODO: if this is going on for too long - stop

        if(rangeCenter > rangeLimit_Warning2 && (rangeLimit_Timestamp + rangeLimit_RotateFor) <= uptime)
        {
            wheelSpinCompleted = true;
            servoRangeDirection = NONE;
        }
    }
}
