#include "Arduino.h"

uint8_t motorPin1_1 = 4;
uint8_t motorPin1_2 = 5;
uint8_t motorPin1_speed = 3;
uint8_t motorPin1_A = A7;

uint8_t motorPin2_1 = 7;
uint8_t motorPin2_2 = 8;
uint8_t motorPin2_speed = 6;
uint8_t motorPin2_A = A6;

uint8_t motorPin3_1 = 10;
uint8_t motorPin3_2 = 11;
uint8_t motorPin3_speed = 9;
uint8_t motorPin3_A = A5;

// ----------

uint16_t motor1_RPMCount = 0;
uint8_t motor1_State = 0;
uint16_t motor1_MaxRPM = 0;

uint16_t motor2_RPMCount = 0;
uint8_t motor2_State = 0;
uint16_t motor2_MaxRPM = 0;

uint16_t motor3_RPMCount = 0;
uint8_t motor3_State = 0;
uint16_t motor3_MaxRPM = 0;

// ----------

// TODO: check if only one would be enough
const int SpeedMappingSize = 101;
uint8_t SpeedMapping_Motor1[SpeedMappingSize];
uint8_t SpeedMapping_Motor2[SpeedMappingSize];
uint8_t SpeedMapping_Motor3[SpeedMappingSize];

// ----------

uint8_t initState = 0;
uint16_t initTimestamp = 0;
uint8_t initSpeed = 255;

// ----------
// ----------

void setup()
{
    Serial.begin(9600);
    while (!Serial)
        ;
    Serial.println("Init");

    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);
    pinMode(motorPin1_speed, OUTPUT);
    pinMode(motorPin1_A, INPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);
    pinMode(motorPin2_speed, OUTPUT);
    pinMode(motorPin2_A, INPUT);

    pinMode(motorPin3_1, OUTPUT);
    pinMode(motorPin3_2, OUTPUT);
    pinMode(motorPin3_speed, OUTPUT);
    pinMode(motorPin3_A, INPUT);

    delay(1000);
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


void Calibration()
{
    if (initState >= 3)
    {
        return;
    }

    uint16_t time = millis();

    if(initState == 0)
    {
        initSpeed = 255;
        SetWheelsTo(initSpeed);

        motor1_RPMCount = 0;
        motor2_RPMCount = 0;
        motor3_RPMCount = 0;

        initTimestamp = time;
        initState = 1;
    }

    uint8_t delta = 250;
    if (initState == 1 && initTimestamp + delta*2 <= time)
    {
        motor1_RPMCount = 0;
        motor2_RPMCount = 0;
        motor3_RPMCount = 0;

        initTimestamp = time;
        initState = 2;
    }


    if (initState == 2 && initTimestamp + delta <= time && initSpeed == 255)
    {
        motor1_MaxRPM = motor1_RPMCount;
        motor2_MaxRPM = motor2_RPMCount;
        motor3_MaxRPM = motor3_RPMCount;
    }

    if (initState == 2 && initTimestamp + delta <= time && initSpeed > 0)
    {
       int smz = SpeedMappingSize-1;
       if(motor1_RPMCount != 0 && motor1_MaxRPM != 0 && SpeedMapping_Motor1[smz * motor1_RPMCount / motor1_MaxRPM] == 0)
       {
             SpeedMapping_Motor1[smz * motor1_RPMCount / motor1_MaxRPM] = initSpeed;
       }

       if(motor2_RPMCount != 0 && motor2_MaxRPM != 0 && SpeedMapping_Motor2[smz * motor2_RPMCount / motor2_MaxRPM] == 0)
       {
             SpeedMapping_Motor2[smz * motor2_RPMCount / motor2_MaxRPM] = initSpeed;
       }

       if(motor3_RPMCount != 0 && motor3_MaxRPM != 0 && SpeedMapping_Motor3[smz * motor3_RPMCount / motor3_MaxRPM] == 0)
       {
             SpeedMapping_Motor3[smz * motor3_RPMCount / motor3_MaxRPM] = initSpeed;
       }


        // 13:  255 - 245 - 235 - 225 - 215 - 205 - 195 - 185 - 175 - 165 - 155 - 145 - 135
        if (initSpeed > 140)
        {
            initSpeed -= 10;
        }

        // 10:  130 - 125 - 120 - 115 - 110 - 105 - 100 - 95 - 90 - 85
        else if (initSpeed > 85)
        {
            initSpeed -= 5;
        }

        // 86:  85 - 0
        else
        {
            initSpeed -= 1;
        }

        SetWheelsTo(initSpeed);
        initTimestamp = time;

        motor1_RPMCount = 0;
        motor2_RPMCount = 0;
       motor3_RPMCount = 0;
    }


    if (initState == 2 && initSpeed == 0)
    {
        initState = 3;
        for(int i = 0; i < SpeedMappingSize; i++)
        {
            Serial.print(i);
            Serial.print(":   ");
            Serial.print(SpeedMapping_Motor1[i]);
            Serial.print(" - ");
            Serial.print(SpeedMapping_Motor2[i]);
            Serial.print(" - ");
            Serial.print(SpeedMapping_Motor3[i]);
            Serial.print("\n");
        }
    }
}


void SetWheelsTo(int speed)
{
    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, speed);
    SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, speed);
    SetMotor(motorPin3_speed, motorPin3_1, motorPin3_2, speed);
}


void UpdateRPM()
{
    int state = (analogRead(motorPin1_A) < 500) ? 0 : 1;
    if(state != motor1_State)
    {
        motor1_RPMCount++;
        motor1_State = state;
    }

    state = (analogRead(motorPin2_A) < 500) ? 0 : 1;
    if(state != motor2_State)
    {
        motor2_RPMCount++;
        motor2_State = state;
    }

    state = (analogRead(motorPin3_A) < 500) ? 0 : 1;
    if(state != motor3_State)
    {
        motor3_RPMCount++;
        motor3_State = state;
    }
}


int WheelMapping(int speed, int wheelID)
{
       if(speed == 0) { return 0; }

       if(wheelID == 1) { return SpeedMapping_Motor1[speed]; }

       if(wheelID == 2) { return SpeedMapping_Motor2[speed]; }

       if(wheelID == 3) { return SpeedMapping_Motor3[speed]; }

       return 0;
}


void loop()
{
    UpdateRPM();

    Calibration();

    //SetWheelsTo(0);
}
