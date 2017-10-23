#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"
#include "ros.h"
#include "ros/time.h"
#include "sensor_msgs/Range.h" // Ultrasonic Range

// ROS
ros::NodeHandle  nh;

sensor_msgs::Range rangeMessage;
ros::Publisher rangePublisher1("/ultrasound/1", &rangeMessage);
ros::Publisher rangePublisher2("/ultrasound/2", &rangeMessage);

const char rangeFrameid[] = "/ultrasound";

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
    nh.advertise(rangePublisher1);
    nh.advertise(rangePublisher2);

    rangeMessage.radiation_type = sensor_msgs::Range::ULTRASOUND;
    rangeMessage.field_of_view = 0.1;
    rangeMessage.min_range = 0.0;
    rangeMessage.max_range = maxDistance/100; // cm to meter
    rangeMessage.header.frame_id = rangeFrameid;

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2350); // 400, 2600 to fix rotation issues
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


void SendServoAngleToROS(int angle)
{

}


void SendDistanceToROS(int sensorID, float rangeInCentimeter)
{
    rangeMessage.range = rangeInCentimeter/100;
    rangeMessage.header.stamp = nh.now();

    if(sensorID == 1)
    {
        rangePublisher1.publish(&rangeMessage);
    }

    if(sensorID == 2)
    {
        rangePublisher2.publish(&rangeMessage);
    }
}


void loop()
{
    long rangeFront = GetRange(1);
    long rangeBack = GetRange(2);

    uint8_t actualServoPos = ServoMotor.read();
    if(servoPos == actualServoPos)
    {
        ServoMotor.write(GetNextServoAngle());
        if(!nh.connected())
        {
            delay(5);
        }
    }

    if(rangeFront > 0)
    {
        SendDistanceToROS(1, rangeFront);
    }

    if(rangeBack > 0)
    {
        SendDistanceToROS(2, rangeBack);
    }

    SendServoAngleToROS(servoPos);

    nh.spinOnce();
}
