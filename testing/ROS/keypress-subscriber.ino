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
    String dataType = data.substring(0,1);
    String dataContent = data.substring(2);
    if(dataType == "D")
    {
        if(dataContent == "273") // UP
        {
            analogWrite(motorPin1_speed, 255);
            analogWrite(motorPin1_1, 255);
            analogWrite(motorPin1_2, 0);
            analogWrite(motorPin2_speed, 255);
            analogWrite(motorPin2_1, 255);
            analogWrite(motorPin2_2, 0);
        }
        else if(dataContent == "274") // DOWN
        {
            analogWrite(motorPin1_speed, 255);
            analogWrite(motorPin1_1, 0);
            analogWrite(motorPin1_2, 255);
            analogWrite(motorPin2_speed, 255);
            analogWrite(motorPin2_1, 0);
            analogWrite(motorPin2_2, 255);
        }
        else if(dataContent == "275") // RIGHT
        {
            analogWrite(motorPin1_speed, 255);
            analogWrite(motorPin1_1, 255);
            analogWrite(motorPin1_2, 0);
        }
        else if(dataContent == "276") // LEFT
        {
            analogWrite(motorPin2_speed, 255);
            analogWrite(motorPin2_1, 255);
            analogWrite(motorPin2_2, 0);        
        }

        /*
        analogWrite(motorPin1_speed, 255);
        analogWrite(motorPin1_1, 255);
        analogWrite(motorPin1_2, 0);
        analogWrite(motorPin2_speed, 255);
        analogWrite(motorPin2_1, 255);
        analogWrite(motorPin2_2, 0);
        */
    }

    if(dataType == "U")
    {
        analogWrite(motorPin1_speed, 0);
        analogWrite(motorPin1_1, 0);
        analogWrite(motorPin1_2, 0);
        analogWrite(motorPin2_speed, 0);
        analogWrite(motorPin2_1, 0);
        analogWrite(motorPin2_2, 0);
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