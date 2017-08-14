#include <ros.h>
#include <std_msgs/String.h>
#include <Arduino.h>

ros::NodeHandle nh;


void messageCb( const std_msgs::String& incoming_msg )
{
    messageTTL = messageTTLInit;

    String data = incoming_msg.data;

    int splitPos = data.indexOf('|');

    String leftData = data.substring(0, splitPos);
    String rightData = data.substring(splitPos+1);


}

ros::Subscriber<std_msgs::String> sub("to_arduino", &messageCb );

void setup()
{
    nh.initNode();
    nh.subscribe(sub);
}

void loop()
{
    nh.spinOnce();
}
