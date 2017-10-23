#include <ros.h>
#include <ros/time.h>
#include <tf/transform_broadcaster.h>
#include "sensor_msgs/Range.h" // Ultrasonic Range

ros::NodeHandle  nh;

sensor_msgs::Range rangeMessage;
ros::Publisher rangePublisher1("/ultrasound/1", &rangeMessage);
ros::Publisher rangePublisher2("/ultrasound/2", &rangeMessage);

const char rangeFrameid[] = "/ultrasound";




geometry_msgs::TransformStamped t;
tf::TransformBroadcaster broadcaster;

char servo_node_1[] = "/servo_node_1";
char servo_node_2[] = "/servo_node_2";
char base_link[] = "/base_link";
char odom[] = "/odom";


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





void setup()
{
    nh.initNode();
    broadcaster.init(nh);

    nh.advertise(rangePublisher1);
    nh.advertise(rangePublisher2);
}

float tempNumber = 0;

void loop()
{
    tempNumber += 0.1;

    t.header.frame_id = odom;
    t.child_frame_id = base_link;
    t.transform.translation.x = 0.0;
    t.transform.translation.y = 0.0;
    t.transform.translation.z = 1.0;

    t.transform.rotation = createQuaternionFromRPY(0.0, 0.0, tempNumber);
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


    rangeMessage.radiation_type = sensor_msgs::Range::ULTRASOUND;
    rangeMessage.field_of_view = 0.1;
    rangeMessage.min_range = 0.0;
    rangeMessage.max_range = 200/100; // cm to meter
    rangeMessage.header.frame_id = servo_node_1;
    rangeMessage.range = 195/100;
    rangeMessage.header.stamp = nh.now();
    rangePublisher1.publish(&rangeMessage);


    rangeMessage.radiation_type = sensor_msgs::Range::ULTRASOUND;
    rangeMessage.field_of_view = 0.1;
    rangeMessage.min_range = 0.0;
    rangeMessage.max_range = 200/100; // cm to meter
    rangeMessage.header.frame_id = servo_node_2;
    rangeMessage.range = 195/100;
    rangeMessage.header.stamp = nh.now();
    rangePublisher2.publish(&rangeMessage);





    nh.spinOnce();
    delay(1);
}
