#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"
#include "ros.h"
#include "ros/time.h"
#include "sensor_msgs/Range.h" // Ultrasonic Range
#include "sensor_msgs/JointState.h" // Servo Angle


// ROS
ros::NodeHandle  nh;

sensor_msgs::Range rangeMessage;
ros::Publisher rangePublisher("/ultrasound", &rangeMessage);

const char rangeFrameid1[] = "/ultrasound/1";
const char rangeFrameid2[] = "/ultrasound/2";


sensor_msgs::JointState jointMessage;
ros::Publisher odometryPublisher("/odometry", &jointMessage);

const char jointFrameid[] = "/ultrasound/joint";
const char *jointNames[] = {"FRONT", "BACK"};


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
    nh.advertise(rangePublisher);
    nh.advertise(odometryPublisher);

    rangeMessage.radiation_type = sensor_msgs::Range::ULTRASOUND;
    rangeMessage.field_of_view = 0.1;
    rangeMessage.min_range = 0.0;
    rangeMessage.max_range = maxDistance/100; // cm to meter


    jointMessage.header.frame_id = jointFrameid;
    jointMessage.name_length = 2;
    //jointMessage.velocity_length = 2;
    jointMessage.position_length = 2;
    //jointMessage.effort_length = 2;

    jointMessage.name = jointNames;


    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2600); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
}


long GetRange(int id)
{
    long range = 0;
    if(id == 1)
    {
        range = sonar1.ping_cm();
    }

    if(id == 2)
    {
        range = sonar2.ping_cm();
    }

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


void SendDistanceToROS(int sensorID, float rangeInCentimeter)
{
    if(sensorID == 1)
    {
        rangeMessage.header.frame_id = rangeFrameid1;
    }

    if(sensorID == 2)
    {
        rangeMessage.header.frame_id = rangeFrameid2;
    }

    rangeMessage.range = rangeInCentimeter/100;
    rangeMessage.header.stamp = nh.now();
    rangePublisher.publish(&rangeMessage);
}


void loop()
{
    long rangeFront = GetRange(1);
    long rangeBack = GetRange(2);

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        ServoMotor.write(GetNextServoAngle());
        //delay(5);
    }

    SendDistanceToROS(1, rangeFront);
    SendDistanceToROS(2, rangeBack);

    // TODO - extra function to send
    float pos[2] = {float(servoPos), float(servoPos+180%360)};
    jointMessage.position = pos;
    jointMessage.header.stamp = nh.now();
    odometryPublisher.publish(&jointMessage);

    nh.spinOnce();
}


