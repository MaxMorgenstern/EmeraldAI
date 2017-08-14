#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

// **********
// Variables
// **********

ros::NodeHandle nh;

String messageData[3];

// **********
// ROS Messages
// **********

void messageCallback( const std_msgs::String& incoming_msg )
{
    messageTTL = messageTTLInit;

    String data = incoming_msg.data;

    int firstDelimiter = data.indexOf('|');
    int secondDelimiter = data.lastIndexOf('|');

    messageData[0] = data.substring(0, firstDelimiter);
    messageData[1] = data.substring(firstDelimiter+1, secondDelimiter);
    messageData[2] = data.substring(secondDelimiter+1);

}

ros::Subscriber<std_msgs::String> sub("to_arduino", &messageCallback );

// **********
// Setup
// **********

void setup()
{
    nh.initNode();
    nh.subscribe(sub);
}

// **********
// Main Loop
// **********

void loop()
{
    nh.spinOnce();
}
