#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a subscriber. Subscribes the IMU readings and save by data_logger_module.

"""

# imports
import rospy
import numpy as np
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_matrix as q2m
from tf.transformations import euler_from_matrix as m2e

import Data.data_logger_module as data_logger

rospy.init_node('data_logger_sub')

# variable definitions

test_angle = Vector3()

q1 = Quaternion()
q2 = Quaternion()
euler_pose_elbow = [0.0, 0.0, 0.0]
euler_pose_wrist = [0.0, 0.0, 0.0]
quat_pose_elbow = Quaternion()
quat_pose_wrist = Quaternion()

R_world2elbow = np.identity(4)

human_joint_info = JointState()
human_joint_info.name = ['human_wrist_pitch', 'human_wrist_roll', 'human_wrist_yaw', 'human_elbow_pitch', 'human_elbow_roll', 'human_elbow_yaw']
human_joint_info.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

calibration_flag = 0
IMU_init = {"quat_pose_elbow": [0.0, 0.0, 0.0, 0.0],
            "quat_pose_wrist": [0.0, 0.0, 0.0, 0.0]}


# Function definitions
def callback_imu_elbow(msg):
    global human_joint_info, R_world2elbow
    while calibration_flag < 10:
        IMU_init["quat_pose_elbow"] = msg.orientation
        # print "calibrating"

    R_init_elbow = q2m([IMU_init["quat_pose_elbow"].x, IMU_init["quat_pose_elbow"].y, IMU_init["quat_pose_elbow"].z, IMU_init["quat_pose_elbow"].w])
    R_current_elbow = q2m([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
    R_world2elbow = np.dot(np.transpose(R_init_elbow), R_current_elbow)

    elbow_angles = m2e(R_world2elbow, axes="sxyz")

    human_joint_info.position[3] = elbow_angles[0]
    human_joint_info.position[4] = elbow_angles[2]
    human_joint_info.position[5] = elbow_angles[1]


def callback_imu_wrist(msg):
    global human_joint_info, R_world2elbow
    while calibration_flag < 10:
        IMU_init["quat_pose_wrist"] = msg.orientation
        print "calibrating"
    R_init_wrist = q2m([IMU_init["quat_pose_wrist"].x, IMU_init["quat_pose_wrist"].y, IMU_init["quat_pose_wrist"].z, IMU_init["quat_pose_wrist"].w])
    R_current_wrist = q2m([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
    R_world2wrist = np.dot(np.transpose(R_init_wrist), R_current_wrist)
    R_elbow2wrist = np.dot(np.transpose(R_world2elbow), R_world2wrist)

    wrist_angles = m2e(R_elbow2wrist, axes="sxyz")
    # print "%5.2f --- %5.2f -- %5.2f" % wrist_angles

    human_joint_info.position[0] = wrist_angles[0]
    human_joint_info.position[1] = wrist_angles[2]
    human_joint_info.position[2] = wrist_angles[1]


if __name__ == '__main__':
    global joint_info
    pub = rospy.Publisher('/joint_states', JointState, queue_size=1)
    pub_test = rospy.Publisher('/test_angle', Vector3, queue_size=1)
    sub_imu_e = rospy.Subscriber('/sensor_l_elbow', Imu, callback_imu_elbow)
    sub_imu_w = rospy.Subscriber('/sensor_l_wrist', Imu, callback_imu_wrist)
    data_logger.enable_logging()
    rate = rospy.Rate(10)
    log_start_time = rospy.get_time()
    while not rospy.is_shutdown():
        human_joint_info.header.stamp = rospy.Time.now()
        # data_logger.log_metrics(tg=rospy.get_time(), te=rospy.get_time()-log_start_time, pitch=human_joint_info.position[0], roll=human_joint_info.position[1], yaw=human_joint_info.position[2], mark="not-aided")
        calibration_flag = calibration_flag + 1
        test_angle.x = np.degrees(human_joint_info.position[0])  # pitch
        test_angle.y = np.degrees(human_joint_info.position[1])  # yaw
        test_angle.z = np.degrees(human_joint_info.position[2])  # roll
        pub_test.publish(test_angle)
        pub.publish(human_joint_info)
        rate.sleep()
