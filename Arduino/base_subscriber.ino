#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

// **********
// Variables
// **********

ros::NodeHandle rosNode;

uint8_t messageData[4];

uint8_t messageTTL = 100;
uint16_t messageTimestamp = 0;

// **********
// ROS Messages
// **********

void rosMessageCallback(const std_msgs::String& incoming_msg )
{
    messageTimestamp = millis();

    String data = incoming_msg.data;

    int firstDelimiter = data.indexOf('|');
    int secondDelimiter = data.indexOf('|', firstDelimiter+1);
    int thirdDelimiter = data.lastIndexOf('|');

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

void SetMotor(uint8_t pinSpeed, uint8_t pin1, uint8_t pin2, uint8_t speed)
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
        // TODO - Update pins
    }
    else
    {
        // TODO - STOP!
    }

    rosNode.spinOnce();
}
