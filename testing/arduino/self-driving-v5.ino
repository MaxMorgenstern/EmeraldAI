#include "Arduino.h"
#include "Adafruit_NeoPixel.h"
#include "Servo.h"

// Base Date
const uint8_t initialDelay = 2500;

// Ranges and Data
const uint8_t rangeLimit_Warning1 = 50;
const uint8_t rangeLimit_Warning2 = 40;
const uint8_t rangeLimit_Warning3 = 25;
const uint8_t rangeLimit_Stop = 15;

const uint16_t rangeLimit_RotateFor = 500;
unsigned long rangeLimit_Timestamp = 0;
bool wheelSpinCompleted = true;


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
        if(ledBatterySaving && i%4 == 0 || !ledBatterySaving)
        {
            LEDStrip.setPixelColor(i, c);
        }
    }
    LEDStrip.show();
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


void SetLightByRange(long range)
{
    uint32_t color = LEDStrip.Color(0, 255, 0);
    if(range < rangeLimit_Warning1) { color = LEDStrip.Color(127, 255, 0);}
    if(range < rangeLimit_Warning2) { color = LEDStrip.Color(255, 255, 0); }
    if(range < rangeLimit_Warning3) { color = LEDStrip.Color(255, 127, 0); }
    if(range < rangeLimit_Stop) { color = LEDStrip.Color(255, 0, 0); }

    ColorSet(color);
}

void ErrorState()
{
    ColorSet(LEDStrip.Color(0, 0, 255));

    SetMotor(motorPin1_1, motorPin1_2, 0);
    SetMotor(motorPin2_1, motorPin2_2, 0);
}

void loop()
{

    CalculateAverageRange();

    /*
    average_Left
    average_Center
    average_Right
    */

    long range = average_Center;

    SetLightByRange(range);

    if(millis() < initialDelay)
    {
        return;
    }

    // maybe wait for x seconds before starting so a full
    // left center right scan can be performed first


    // obstacle is further away than X cm
    if(wheelSpinCompleted && range > rangeLimit_Stop)
    {
        // drive
        SetMotor(motorPin1_1, motorPin1_2, 255);
        SetMotor(motorPin2_1, motorPin2_2, 255);

        rangeLimit_Timestamp = millis();
    }
    else
    {

        // TODO

        // rotate
        SetMotor(motorPin1_1, motorPin1_2, -255);
        SetMotor(motorPin2_1, motorPin2_2, 255);

        wheelSpinCompleted = false;

        if(range > rangeLimit_Warning3 && (rangeLimit_Timestamp + rangeLimit_RotateFor) <= millis())
        {
            wheelSpinCompleted = true;
        }
    }
}

