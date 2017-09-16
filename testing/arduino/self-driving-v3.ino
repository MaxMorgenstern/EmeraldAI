#include "Arduino.h"
#include "Adafruit_NeoPixel.h"

// defines pins numbers
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;

const uint8_t ledPin = 11;

Adafruit_NeoPixel LEDStrip = Adafruit_NeoPixel(26, ledPin, NEO_GRB + NEO_KHZ800);

const uint8_t motorPin1_1 = 4;
const uint8_t motorPin1_2 = 5;

const uint8_t motorPin2_1 = 7;
const uint8_t motorPin2_2 = 8;


const uint8_t motorEnablePin = 3;

const uint8_t rangeLimit_Stop = 40;
const uint8_t rangeLimit_Warning1 = 90;
const uint8_t rangeLimit_Warning2 = 70;
const uint8_t rangeLimit_Warning3 = 50;

bool spinCompleted = true;


void setup()
{
    // Scanner
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input


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
}


long MicrosecondsToCentimeters(long microseconds)
{
    return microseconds / 29 / 2;
}


// Use library to minimize delay
float GetUltrasoundRange()
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



void colorSet(uint32_t c) {
    for(uint16_t i=0; i < LEDStrip.numPixels(); i++)
    {
        LEDStrip.setPixelColor(i, c);
    }
    LEDStrip.show();
}


void loop()
{
    long range = GetUltrasoundRange();

    int motorSpeed = 1 * 255;
    uint32_t color = LEDStrip.Color(0, 255, 0);
    if(range < rangeLimit_Warning1) { motorSpeed = 0.6 * 255; color = LEDStrip.Color(127, 255, 0);}
    if(range < rangeLimit_Warning2) { motorSpeed = 0.5 * 255; color = LEDStrip.Color(255, 255, 0); }
    if(range < rangeLimit_Warning3) { motorSpeed = 0.4 * 255; color = LEDStrip.Color(255, 127, 0); }
    if(range < rangeLimit) { color = LEDStrip.Color(255, 0, 0); }

    colorSet(color);

    // obstacle is further away than X cm
    if(spinCompleted && range > 0 && range > rangeLimit)
    {
        // drive
        SetMotor(motorPin1_1, motorPin1_2, motorSpeed);
        SetMotor(motorPin2_1, motorPin2_2, motorSpeed);
    }
    else
    {
        spinCompleted = false;

        // rotate
        SetMotor(motorPin1_1, motorPin1_2, -motorSpeed);
        SetMotor(motorPin2_1, motorPin2_2, motorSpeed);

        if(range > (rangeLimit * 2))
        {
            spinCompleted = true;
        }
    }
}

