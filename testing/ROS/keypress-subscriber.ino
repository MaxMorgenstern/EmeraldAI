#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

int motorPin1_1 = 8;
int motorPin1_2 = 9;
int motorPin1_speed = 5;

int motorPin2_1 = 10;
int motorPin2_2 = 11;
int motorPin2_speed = 4;

ros::NodeHandle nh;

void messageCb( const std_msgs::String& incoming_msg )
{
    String data = incoming_msg.data;

    if(data == "0") // No movement
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 0, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 0, true);
    }
    else if(data == "1") // Right
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 0, true);
    }
    else if(data == "2") // Left
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 0, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255, true);
    }
    else if(data == "4") // Down
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255, false);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255, false);
    }
    else if(data == "8") // Up
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255, true);
    }
    else if(data == "5") // Down Right
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255, false);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 126, false);
    }
    else if(data == "6") // Down Left
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 126, false);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255, false);
    }
    else if(data == "9") // Up Right
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 255, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 126, true);
    }
    else if(data == "10") // Up Left
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 126, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 255, true);
    }
    else // ERROR --> STOP
    {
        SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, 0, true);
        SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, 0, true);
    }
}

void SetMotor(int pinSpeed, int pin1, int pin2, int speed, bool forward)
{
    analogWrite(pinSpeed, speed);
    if (forward)
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
    nh.spinOnce();
    delay(200); 
}