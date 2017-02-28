#include <ros.h>
#include <std_msgs/String.h>

ros::NodeHandle  nh;

std_msgs::String str_msg;
ros::Publisher chatter("from_arduino", &str_msg);

void messageCb( const std_msgs::String& incoming_msg )
{
  str_msg.data = incoming_msg.data; 
  chatter.publish( &str_msg ); 
}

ros::Subscriber<std_msgs::String> sub("to_arduino", &messageCb );

void setup()
{
  nh.initNode();
  nh.advertise(chatter);
  nh.subscribe(sub);
}

void loop()
{
  nh.spinOnce();
  delay(200); 
}