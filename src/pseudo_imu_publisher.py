#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Publish a pseudo IMU data like a bag file.
"""

import rospy
# from std_msgs.msg import Header
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
    pub_imu1 = rospy.Publisher('/pseudo_imu1_msg', Imu, queue_size=10)
    pub_imu2 = rospy.Publisher('/pseudo_imu2_msg', Imu, queue_size=10)
    rospy.init_node('pseudo_imu_msg_creator', anonymous=False)
    rate = rospy.Rate(10)  # 10hz
    imu1_data = Imu()
    imu2_data = Imu()
    index = 0.0
    while not rospy.is_shutdown():
        # imu_data.header = Header()
        imu1_data.header.stamp = rospy.Time.now()
        imu1_data.header.frame_id = "imu1_data"
        imu1_data.orientation.x = 0.0
        imu1_data.orientation.y = 0.0
        imu1_data.orientation.z = 0.0
        imu1_data.orientation.w = 1.0
        imu1_data.orientation_covariance[0] = -1.0
        imu1_data.angular_velocity.x = 10.0
        imu1_data.angular_velocity.y = 0.0
        imu1_data.angular_velocity.z = 0.0
        # imu_data.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        imu1_data.linear_acceleration.x = 0.0
        imu1_data.linear_acceleration.y = 0.0
        imu1_data.linear_acceleration.z = 0.0
        # imu_data.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        imu2_data.header.stamp = rospy.Time.now()
        imu2_data.header.frame_id = "imu2_data"
        imu2_data.orientation.x = 0.0
        imu2_data.orientation.y = 0.0
        imu2_data.orientation.z = 0.0
        imu2_data.orientation.w = 1.0
        imu2_data.orientation_covariance[0] = -1.0
        imu2_data.angular_velocity.x = 20.0
        imu2_data.angular_velocity.y = 0.0
        imu2_data.angular_velocity.z = 0.0
        # imu_data.angular_velocity_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        imu2_data.linear_acceleration.x = 0.0
        imu2_data.linear_acceleration.y = 0.0
        imu2_data.linear_acceleration.z = 0.0
        # imu_data.linear_acceleration_covariance = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        rospy.loginfo("started")
        pub_imu1.publish(imu1_data)
        pub_imu2.publish(imu2_data)
        rate.sleep()
        index = 0 if index >= 250.0 else index + 0.5


if __name__ == '__main__':
    try:
        pseudo_imu_msg_creator()
    except rospy.ROSInterruptException:
        pass
