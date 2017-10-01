#include "Arduino.h"
#include "Adafruit_NeoPixel.h"
#include "Servo.h"
#include "NewPing.h"

// Base Date
const uint16_t initialDelay = 2500;

// Ranges and Data
const uint8_t rangeLimit_Warning1 = 50;
const uint8_t rangeLimit_Warning2 = 40;
const uint8_t rangeLimit_Warning3 = 25;
const uint8_t rangeLimit_Stop = 15;

const uint16_t rangeLimit_RotateFor = 1000;
unsigned long rangeLimit_Timestamp = 0;
bool wheelSpinCompleted = true;


// Ultrasonic Sensor
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;
const uint16_t maxDistance = 300;

NewPing sonar(trigPin, echoPin, maxDistance);

long rangeLeft;
long rangeCenter;
long rangeRight;

// LED
const uint8_t ledPin = 11;
const bool ledBatterySaving = true;
Adafruit_NeoPixel LEDStrip = Adafruit_NeoPixel(26, ledPin, NEO_GRB + NEO_KHZ800);

// Motor / Wheels
const uint8_t motorPin1_1 = 4;
const uint8_t motorPin1_2 = 5;

const uint8_t motorPin2_1 = 7;
const uint8_t motorPin2_2 = 8;

const uint8_t motorEnablePin = 3;

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
uint8_t servoPos = 90;

uint8_t servoLimitLeft = 10;
uint8_t servoTiltLeft = 50;
uint8_t servoLimitRight = 170;
uint8_t servoTiltRight = 130;
uint8_t servoCenter = 90;



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

    Serial.begin(9600); // Starts the serial communication

    LEDStrip.begin();
    LEDStrip.show(); // Initialize all pixels to 'off'

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin);
    ServoMotor.write(servoPos);
}

void GetRange()
{
    long range = sonar.ping_cm();;

    if(servoPos == servoCenter)
    {
        rangeCenter = range;
    }

    if(servoPos < servoCenter)
    {
        rangeLeft = range;
    }

    if(servoPos > servoCenter)
    {
        rangeRight = range;
    }
}

void SetServoAngle(uint8_t angle)
{
    ServoMotor.write(angle);
    delay(20);
    servoPos = angle;
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

void SetLightErrorState()
{
    ColorSet(LEDStrip.Color(0, 0, 255));

    SetMotor(motorPin1_1, motorPin1_2, 0);
    SetMotor(motorPin2_1, motorPin2_2, 0);
}

void loop()
{

    uint32_t uptime = millis();
    GetRange()

    if(uptime % 5000 == 0)
    {
        SetServoAngle(servoTiltRight)
    }

    if(uptime % 5500 == 0)
    {
        SetServoAngle(servoCenter)
    }


    if(uptime % 9000 == 0)
    {
        SetServoAngle(servoTiltLeft)
    }

    if(uptime % 9500 == 0)
    {
        SetServoAngle(servoCenter)
    }

    // Wait for initial scans before performing any actions
    if(uptime < initialDelay)
    {
        SetLightErrorState();
        return;
    }

    SetLightByRange(rangeCenter);

    // obstacle is further away than X cm
    if(wheelSpinCompleted && rangeCenter > rangeLimit_Stop)
    {
        // drive
        SetMotor(motorPin1_1, motorPin1_2, 255);
        SetMotor(motorPin2_1, motorPin2_2, 255);

        rangeLimit_Timestamp = uptime;
    }

    // TODO - slightly turn if side better than center

    else
    {
        if(rangeLeft > rangeRight)
        {
            SetMotor(motorPin1_1, motorPin1_2, 255);
            SetMotor(motorPin2_1, motorPin2_2, -255);
        }
        else
        {
            SetMotor(motorPin1_1, motorPin1_2, -255);
            SetMotor(motorPin2_1, motorPin2_2, 255);
        }

        wheelSpinCompleted = false;

        if(rangeCenter > rangeLimit_Warning3 && (rangeLimit_Timestamp + rangeLimit_RotateFor) <= uptime)
        {
            wheelSpinCompleted = true;
        }
    }
}

