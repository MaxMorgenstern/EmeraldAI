#include "Arduino.h"
#include "NewPing.h"

// defines pins numbers
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;
const uint8_t maxSenstorDistance = 200; // cm

const uint8_t motorPin1_1 = 4;
const uint8_t motorPin1_2 = 5;
const uint8_t motorPin1_speed = 3;
const uint8_t motorPin1_A = A7;

const uint8_t motorPin2_1 = 7;
const uint8_t motorPin2_2 = 8;
const uint8_t motorPin2_speed = 6;
const uint8_t motorPin2_A = A6;

/*
const uint8_t motorPin3_1 = 10;
const uint8_t motorPin3_2 = 11;
const uint8_t motorPin3_speed = 9;
const uint8_t motorPin3_A = A5;
*/

const uint8_t rangeLimit = 15;

bool spinCompleted = true;
uint8_t nullResultCount = 0;

NewPing sensor1(trigPin, echoPin, maxSenstorDistance);


void setup()
{
    // Motor
    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);
    pinMode(motorPin1_speed, OUTPUT);
    pinMode(motorPin1_A, INPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);
    pinMode(motorPin2_speed, OUTPUT);
    pinMode(motorPin2_A, INPUT);

    /*
    pinMode(motorPin3_1, OUTPUT);
    pinMode(motorPin3_2, OUTPUT);
    pinMode(motorPin3_speed, OUTPUT);
    pinMode(motorPin3_A, INPUT);
	*/

    Serial.begin(9600); // Starts the serial communication
}


void SetMotor(int pinSpeed, int pin1, int pin2, int speed)
{
    analogWrite(pinSpeed, abs(speed));
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


void loop()
{
	long range = sensor1.ping_cm()
	if (range == 0)
	{
		nullResultCount++;
		if(nullResultCount < 10)
		{
			delay(30);
			return;
		}
	}

	// obstacle is further away than X cm
	if(spinCompleted && range > 0 && range > rangeLimit)
	{
		nullResultCount = 0;

		// drive
	    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255);
	    SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255);
    	//SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, 0);
	}
	else
	{
		spinCompleted = false;

		// rotate
	    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255);
    	SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 0);
    	//SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, 0);

    	if(range > (rangeLimit * 2))
    	{
    		spinCompleted = true;
    	}
	}

	delay(50);  // 29ms should be min between scans
}

