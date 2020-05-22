#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Publish a pseudo IMU data like a bag file.
"""

import rospy
from std_msgs.msg import Header
from std_msgs.msg import String
from sensor_msgs.msg import Imu


def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()


def pseudo_imu_msg_creator():
    pub_imu = rospy.Publisher('/pseudo_imu_msg', Imu, queue_size=10)
    rospy.init_node('pseudo_imu_msg_creator', anonymous=False)
    rate = rospy.Rate(10)  # 10hz
    imu_data = Imu()
    index = 0.0
    while not rospy.is_shutdown():
        # imu_data.header = Header()
        imu_data.header.stamp = rospy.Time.now()
        imu_data.header.frame_id = "imu_data"
        # imu_data.orientation.x = 0.0
        # imu_data.orientation.y = 0.0
        # imu_data.orientation.z = 0.0
        # imu_data.orientation.w = 1.0
        imu_data.orientation_covariance[0] = -1.0
        imu_data.angular_velocity.x = index
        imu_data.angular_velocity.y = 0.0
        imu_data.angular_velocity.z = 0.0
        # imu_data.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        imu_data.linear_acceleration.x = 0.0
        imu_data.linear_acceleration.y = 0.0
        imu_data.linear_acceleration.z = 0.0
        # imu_data.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        rospy.loginfo(imu_data)
        pub_imu.publish(imu_data)
        rate.sleep()
        index = 0 if index >= 250.0 else index + 0.5


if __name__ == '__main__':
    try:
        pseudo_imu_msg_creator()
    except rospy.ROSInterruptException:
        pass
