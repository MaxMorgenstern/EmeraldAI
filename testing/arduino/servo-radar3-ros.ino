#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"
#include "ros.h"
#include "ros/time.h"
#include "sensor_msgs/Range.h"

// ROS
ros::NodeHandle  nh;

sensor_msgs::Range range_msg;
ros::Publisher pub_range("/ultrasound", &range_msg);

char frameid[] = "/ultrasound";


// Ultrasonic Sensor
const uint16_t maxDistance = 250;

// Ultrasonic Sensor #1
const uint8_t trigPin = 9;
const uint8_t echoPin = 10;

NewPing sonar1(trigPin, echoPin, maxDistance);

// Ultrasonic Sensor #2
const uint8_t trigPin2 = 11;
const uint8_t echoPin2 = 12;

NewPing sonar2(trigPin2, echoPin2, maxDistance);

// Ultrasonic Servo
Servo ServoMotor;
const uint8_t servoPin = 6;
const uint8_t servoRotationAngel = 5;

enum direction {
  left,
  center,
  right
};

uint8_t servoPos = 90;
direction servoMovement = right;


void setup()
{
    nh.initNode();
    nh.advertise(pub_range);

    range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
    range_msg.header.frame_id =  frameid;
    range_msg.field_of_view = 0.1;  // dummy
    range_msg.min_range = 0.0;
    range_msg.max_range = maxDistance/100;

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2600);
    ServoMotor.write(servoPos);
}


long GetRange1()
{
    long range = sonar1.ping_cm();

    // fallback if return value is out of range
    if(range == 0) { range = maxDistance; }

    return range;
}

long GetRange2()
{
    long range = sonar2.ping_cm();

    // fallback if return value is out of range
    if(range == 0) { range = maxDistance; }

    return range;
}


uint8_t GetNextServoAngle()
{
    if(servoPos <= 0)
    {
        servoMovement = right;
        servoPos = 0;
    }

    if(servoPos >= 180)
    {
        servoMovement = left;
        servoPos = 180;
    }


    if(servoMovement == right)
    {
        servoPos += servoRotationAngel;
    }
    else
    {
        servoPos -= servoRotationAngel;
    }

    return servoPos;
}

void SendDistance(float range_in_centimeter)
{
    range_msg.range = range_in_centimeter/100;
    range_msg.header.stamp = nh.now();
    pub_range.publish(&range_msg);
}


void loop()
{
    long range1 = GetRange1();
    long range2 = GetRange2();

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        ServoMotor.write(GetNextServoAngle());
        delay(5);
    }

    SendDistance(range1);
    //SendDistance(range2);

    nh.spinOnce();
}


