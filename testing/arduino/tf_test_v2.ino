#include "Arduino.h"
#include "Servo.h"
#include "NewPing.h"
#include "ros.h"
#include "ros/time.h"
#include "tf/transform_broadcaster.h"
#include "sensor_msgs/Range.h" // Ultrasonic Range

ros::NodeHandle  nh;

geometry_msgs::TransformStamped t;
tf::TransformBroadcaster broadcaster;

char servo_node_1[] = "/servo_node_1";
char servo_node_2[] = "/servo_node_2";
char base_link[] = "/base_link";
char odom[] = "/odom";

sensor_msgs::Range rangeMessage;
ros::Publisher rangePublisher1("/ultrasound/1", &rangeMessage);
ros::Publisher rangePublisher2("/ultrasound/2", &rangeMessage);


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

// ------------------------------
//            SETUP
// ------------------------------

void setup()
{
    nh.initNode();
    broadcaster.init(nh);

    nh.advertise(rangePublisher1);
    nh.advertise(rangePublisher2);

    rangeMessage.radiation_type = sensor_msgs::Range::ULTRASOUND;
    rangeMessage.field_of_view = 0.1;
    rangeMessage.min_range = 0.0;
    rangeMessage.max_range = maxDistance/100; // cm to meter

    // attach servo pin and set to initial direction
    ServoMotor.attach(servoPin, 400, 2350); // 400, 2600 to fix rotation issues
    ServoMotor.write(servoPos);
}


// ------------------------------


static geometry_msgs::Quaternion createQuaternionFromRPY(double roll, double pitch, double yaw) {
    geometry_msgs::Quaternion q;
    double t0 = cos(yaw * 0.5);
    double t1 = sin(yaw * 0.5);
    double t2 = cos(roll * 0.5);
    double t3 = sin(roll * 0.5);
    double t4 = cos(pitch * 0.5);
    double t5 = sin(pitch * 0.5);
    q.w = t0 * t2 * t4 + t1 * t3 * t5;
    q.x = t0 * t3 * t4 - t1 * t2 * t5;
    q.y = t0 * t2 * t5 + t1 * t3 * t4;
    q.z = t1 * t2 * t4 - t0 * t3 * t5;
    return q;
}

double RadianToDegree(double rad)
{
    return (rad * 4068) / 71.0;
}

double DegreeToRadian(double deg)
{
    return (deg * 71) / 4068.0;
}


// ------------------------------



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

void SendTransformToROS()
{

}


void SendDistanceToROS(int sensorID, float rangeInCentimeter)
{
    rangeMessage.range = rangeInCentimeter/100;
    rangeMessage.header.stamp = nh.now();

    if(sensorID == 1)
    {
        rangeMessage.header.frame_id = servo_node_1;
        rangePublisher1.publish(&rangeMessage);
    }

    if(sensorID == 2)
    {
        rangeMessage.header.frame_id = servo_node_2;
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








    t.header.frame_id = odom;
    t.child_frame_id = base_link;
    t.transform.translation.x = 0.0;
    t.transform.translation.y = 0.0;
    t.transform.translation.z = 1.0;

    t.transform.rotation = createQuaternionFromRPY(0.0, 0.0, DegreeToRadian(servoPos));
    /*
    t.transform.rotation.x = 0.0;
    t.transform.rotation.y = 0.0;
    t.transform.rotation.z = 0.0;
    t.transform.rotation.w = 1.0;
    */

    t.header.stamp = nh.now();

    broadcaster.sendTransform(t);


    t.header.frame_id = base_link;
    t.child_frame_id = servo_node_1;
    t.transform.translation.x = 0.0;
    t.transform.translation.y = 0.05;
    t.transform.translation.z = 0.0;

    /// radian = (degree * 71) / 4068.0
    /// degree = (radians * 4068) / 71.0

    t.transform.rotation = createQuaternionFromRPY(0.0, 0.0, ((90 * 71) / 4068.0));
    t.header.stamp = nh.now();

    broadcaster.sendTransform(t);


    t.header.frame_id = base_link;
    t.child_frame_id = servo_node_2;
    t.transform.translation.x = 0.0;
    t.transform.translation.y = -0.05;
    t.transform.translation.z = 0.0;
    t.transform.rotation = createQuaternionFromRPY(0.0, 0.0, ((-90 * 71) / 4068.0));
    t.header.stamp = nh.now();

    broadcaster.sendTransform(t);




    nh.spinOnce();
}
