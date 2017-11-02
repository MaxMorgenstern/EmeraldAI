#include <ros.h>
#include <ros/time.h>
#include <tf/transform_broadcaster.h>

ros::NodeHandle  nh;

geometry_msgs::TransformStamped t;
tf::TransformBroadcaster broadcaster;

char max_was_here[] = "/max_was_here";
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
    t.child_frame_id = max_was_here;
    t.transform.translation.x = 0.0;
    t.transform.translation.y = 1.0;
    t.transform.translation.z = 0.0;

    t.transform.rotation = createQuaternionFromRPY(0.0, 0.0, 0.0);
    /*
    t.transform.rotation.x = 0.0;
    t.transform.rotation.y = 0.0;
    t.transform.rotation.z = 0.0;
    t.transform.rotation.w = 1.0;
    */

    t.header.stamp = nh.now();

    broadcaster.sendTransform(t);
    nh.spinOnce();


    delay(1);
}
