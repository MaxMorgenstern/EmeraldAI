#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

// **********
// Variables
// **********

ros::NodeHandle rosNode;

int messageData[4];

uint8_t messageTTL = 100;
int messageTimestamp = 0;

// Speed Pin, Pin A, Pin B
uint8_t motor_0[] = {3, 4, 5};
uint8_t motor_1[] = {6, 7, 8};
uint8_t motor_2[] = {0, 0, 0};
uint8_t motor_3[] = {0, 0, 0};

// **********
// ROS Messages
// **********

void rosMessageCallback(const std_msgs::String& incoming_msg )
{
    messageTimestamp = millis();

    String data = incoming_msg.data;

    uint8_t firstDelimiter = data.indexOf('|');
    uint8_t secondDelimiter = data.indexOf('|', firstDelimiter+1);
    uint8_t thirdDelimiter = data.lastIndexOf('|');

    messageData[0] = data.substring(0, firstDelimiter).toInt();
    messageData[1] = data.substring(firstDelimiter+1, secondDelimiter).toInt();
    if(secondDelimiter == thirdDelimiter)
    {
        messageData[2] = data.substring(secondDelimiter+1).toInt();
        messageData[3] = 0;
    }
    else
    {
        messageData[2] = data.substring(secondDelimiter+1, thirdDelimiter).toInt();
        messageData[3] = data.substring(thirdDelimiter+1).toInt();
    }
}

ros::Subscriber<std_msgs::String> rosSubscriber("to_arduino", &rosMessageCallback );


// **********
// Motor
// **********

void SetMotorSimple(uint8_t motor[], int speed)
{
    if (motor[0] == 0 and motor[1] == 0 motor[2] == 0) { return; }

    SetMotor(motor[0], motor[1], motor[2], speed);
}

void SetMotor(uint8_t pinSpeed, uint8_t pin1, uint8_t pin2, int speed)
{
    analogWrite(pinSpeed, abs(speed));
    if (speed == 0)
    {
        analogWrite(pin1, 0);
        analogWrite(pin2, 0);
        return;
    }

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
}

// **********
// Setup
// **********

void setup()
{
    rosNode.initNode();
    rosNode.subscribe(rosSubscriber);
}

// **********
// Main Loop
// **********

void loop()
{
    if(messageTimestamp + messageTTL > millis())
    {
        SetMotorSimple(motor_0, messageData[0]);
        SetMotorSimple(motor_1, messageData[1]);
        SetMotorSimple(motor_2, messageData[2]);
        SetMotorSimple(motor_3, messageData[3]);
    }
    else
    {
        SetMotorSimple(motor_0, 0);
        SetMotorSimple(motor_1, 0);
        SetMotorSimple(motor_2, 0);
        SetMotorSimple(motor_3, 0);
    }

    rosNode.spinOnce();
}
