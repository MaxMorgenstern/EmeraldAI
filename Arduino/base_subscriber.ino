#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

// **********
// Variables
// **********

ros::NodeHandle rosNode;

uint8_t messageData[4];

uint8_t messageTTL = 10;
uint16_t messageTimestamp = 0;

// **********
// ROS Messages
// **********

void rosMessageCallback( const std_msgs::String& incoming_msg )
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
    }
    else
    {
        messageData[2] = data.substring(secondDelimiter+1, thirdDelimiter).toInt();
        messageData[3] = data.substring(thirdDelimiter+1).toInt();
    }
}

ros::Subscriber<std_msgs::String> rosSubscriber("to_arduino", &rosMessageCallback );


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
    rosNode.spinOnce();
}
