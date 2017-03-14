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

    int splitPos = data.indexOf('|');

    String leftData = data.substring(0, splitPos);
    String rightData = data.substring(splitPos+1);

    char buffer[10];
    leftData.toCharArray(buffer, 10);
    float leftValue = atof(buffer);
    
    rightData.toCharArray(buffer, 10);
    float rightValue = atof(buffer);
    
    bool leftForward = true;
    if (leftValue < 0)
    {
      leftForward = false;
    }
    
    bool rightForward = true;
    if (rightValue < 0)
    {
      rightForward = false;
    }
    
    SetMotor(motorPin1_speed, motorPin1_1, motorPin1_2, int(255 * leftValue / 100), leftForward);
    SetMotor(motorPin2_speed, motorPin2_1, motorPin2_2, int(255 * rightValue / 100), rightForward);

}




// Invert forward
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
    nh.spinOnce();
    delay(200); 
}