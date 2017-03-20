#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

int motorPin1_1 = 8;
int motorPin1_2 = 9;
int motorPin1_speed = 5;

int motorPin2_1 = 10;
int motorPin2_2 = 11;
int motorPin2_speed = 6;

int globalSpeedInit = 255;
int globalSpeedMin = 50;
int globalSpeedMax = 70;


int targetSpeedLeft = 0;
int targetSpeedRight = 0;

int currentSpeedLeft = 0;
int currentSpeedRight = 0;

bool leftForward = true;
bool rightForward = true;

int messageTTLInit = 10;
int messageTTL = 0;

ros::NodeHandle nh;


void messageCb( const std_msgs::String& incoming_msg )
{
    messageTTL = messageTTLInit;

    String data = incoming_msg.data;

    int splitPos = data.indexOf('|');

    String leftData = data.substring(0, splitPos);
    String rightData = data.substring(splitPos+1);

    char buffer[10];
    leftData.toCharArray(buffer, 10);
    float leftValue = atof(buffer);
    
    rightData.toCharArray(buffer, 10);
    float rightValue = atof(buffer);
    

    leftForward = (leftValue >= 0);
    rightForward = (rightValue >= 0);
    
    targetSpeedLeft = abs((globalSpeedMax - globalSpeedMin) * leftValue / 100);
    targetSpeedLeft += (targetSpeedLeft != 0) ? globalSpeedMin : 0;
    
    targetSpeedRight = abs((globalSpeedMax - globalSpeedMin) * rightValue / 100);
    targetSpeedRight += (targetSpeedRight != 0) ? globalSpeedMin : 0;
}



void SetMotor(int pinSpeed, int pin1, int pin2, int speed, bool forward)
{   
    analogWrite(pinSpeed, speed);
    if (!forward)
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

ros::Subscriber<std_msgs::String> sub("to_arduino", &messageCb );

void setup()
{
    pinMode(motorPin1_1, OUTPUT);
    pinMode(motorPin1_2, OUTPUT);
    pinMode(motorPin1_speed, OUTPUT);

    pinMode(motorPin2_1, OUTPUT);
    pinMode(motorPin2_2, OUTPUT);
    pinMode(motorPin2_speed, OUTPUT);
    
    nh.initNode();
    nh.subscribe(sub);
}

void loop()
{
    if (currentSpeedLeft == 0 && targetSpeedLeft > 0)
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, globalSpeedInit, leftForward);
    }
    
    if (currentSpeedRight == 0 && targetSpeedRight > 0)
    {
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, globalSpeedInit, leftForward);
    }

    if (currentSpeedLeft == 0 && targetSpeedLeft > 0 || currentSpeedRight == 0 && targetSpeedRight > 0 )
    {
        delay(10);
    }

    messageTTL--;
    if (messageTTL <= 0)
    {
        targetSpeedLeft = 0;
        targetSpeedRight = 0;
    }

    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, targetSpeedLeft, leftForward);
    SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, targetSpeedRight, rightForward);

    nh.spinOnce();
    delay(100); 
}