#!/usr/bin/python
import rospy
import tf
import math
import time
import os
from sensor_msgs.msg import Imu

print str(os.getpid())

rospy.init_node('imu_dummy_node', anonymous=False)

imu = Imu()
imu.orientation_covariance = [1e-6, 0, 0, 0, 1e-6, 0, 0, 0, 1e-6]
imu.angular_velocity_covariance = [1e-6, 0, 0, 0, 1e-6, 0, 0, 0, 1e-6]
imu.linear_acceleration_covariance = [1e-6, 0, 0, 0, 1e-6, 0, 0, 0, 1e-6]

imu_pub = rospy.Publisher('imu', Imu, queue_size=10)


imu.header.stamp = rospy.Time.now()
quaternion = tf.transformations.quaternion_from_euler(-25.35, -9.48, -26.90)

imu.orientation.x = quaternion[0]
imu.orientation.y = quaternion[1]
imu.orientation.z = quaternion[2]
imu.orientation.w = quaternion[3]

imu.angular_velocity.x = 5.13*10*math.pi/180
imu.angular_velocity.y = -2.93*10*math.pi/180
imu.angular_velocity.z = 2.63*10*math.pi/180

"""
imu.orientation.x = data["QUATERNION_Q0"]
imu.orientation.y = data["QUATERNION_Q1"]
imu.orientation.z = data["QUATERNION_Q2"]
imu.orientation.w = data["QUATERNION_Q3"]
imu.linear_acceleration.x = data["ACCEL_X_FILTERED"]/4096.0*9.8
imu.linear_acceleration.y = data["ACCEL_Y_FILTERED"]/4096.0*9.8
imu.linear_acceleration.z = data["ACCEL_Z_FILTERED"]/4096.0*9.8
imu.angular_velocity.x = data["GYRO_X_FILTERED"]*10*math.pi/180
imu.angular_velocity.y = data["GYRO_Y_FILTERED"]*10*math.pi/180
imu.angular_velocity.z = data["GYRO_Z_FILTERED"]*10*math.pi/180

"""

while True:
	imu_pub.publish(imu)
	time.sleep(1)
	pass
