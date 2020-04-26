#!/usr/bin/env python

"""
This is a subscriber. Subscribes the IMU readings and save into data_logger_module.

"""

# imports
import Data.data_logger_module as data_logger

import rospy
import numpy as np
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_matrix as q2m
from tf.transformations import euler_from_matrix as m2e


class IMUdataRecorder:
    def __init__(self, rate=30):
        """Initializes the IMU data recording node.
        @param DataLogger: the data logger object"""
        rospy.init_node("data_logger_sub")
        self.r = rospy.Rate(rate)
        self. euler_pose_elbow = [0.0, 0.0, 0.0]
        self.euler_pose_wrist = [0.0, 0.0, 0.0]
        self.quat_pose_elbow = Quaternion()
        self.quat_pose_wrist = Quaternion()
        self.R_world2elbow = np.identity(4)
        self.human_joint_info = JointState()
        self.human_joint_info.name = ['human_wrist_pitch', 'human_wrist_roll', 'human_wrist_yaw', 'human_elbow_pitch', 'human_elbow_roll', 'human_elbow_yaw']
        self.human_joint_info.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        self.calibration_flag = 0
        self.IMU_init = {"quat_pose_elbow": [0.0, 0.0, 0.0, 0.0], "quat_pose_wrist": [0.0, 0.0, 0.0, 0.0]}
        self.pub = rospy.Publisher('/joint_states', JointState, queue_size=1)
        self.sub_imu_e = rospy.Subscriber('/sensor_l_elbow', Imu, self.callback_imu_elbow)
        self.sub_imu_w = rospy.Subscriber('/sensor_l_wrist', Imu, self.callback_imu_wrist)
        self.log_start_time = rospy.get_time()

    def data_logger_enabler(self):
        data_logger.enable_logging()

    def update(self):
        self.calculate_angles()
        self.human_joint_info.header.stamp = rospy.Time.now()
        data_logger.log_metrics(tg=rospy.get_time(), te=rospy.get_time()-self.log_start_time, pitch=self.human_joint_info.position[0], roll=self.human_joint_info.position[1], yaw=self.human_joint_info.position[2], mark="not-aided")
        self.calibration_flag = self.calibration_flag + 1
        self.pub.publish(self.human_joint_info)
        self.r.sleep()

    def cb_imu_elbow(self, msg):
        self.elbow_measurement = msg

    def cb_imu_wrist(self, msg):
        self.wrist_measurement = msg

    def calculate_angles(self):
        while self.calibration_flag < 10:
            self.IMU_init["quat_pose_elbow"] = self.elbow_measurement
            self.IMU_init["quat_pose_wrist"] = self.wrist_measurement

        # Initial measurements for calibration
        self.R_init_elbow = q2m([self.IMU_init["quat_pose_elbow"].x, self.IMU_init["quat_pose_elbow"].y, self.IMU_init["quat_pose_elbow"].z, self.IMU_init["quat_pose_elbow"].w])

        self.R_init_wrist = q2m([self.IMU_init["quat_pose_wrist"].x, self.IMU_init["quat_pose_wrist"].y, self.IMU_init["quat_pose_wrist"].z, self.IMU_init["quat_pose_wrist"].w])

        # Current Measurements
        self.R_current_elbow = q2m([self.elbow_measurement.orientation.x, self.elbow_measurement.orientation.y, self.elbow_measurement.orientation.z, self.elbow_measurement.orientation.w])

        self.R_current_wrist = q2m([self.wrist_measurement.orientation.x, self.wrist_measurement.orientation.y, self.wrist_measurement.orientation.z, self.wrist_measurement.orientation.w])

        # Rotation matrices
        self.R_world2elbow = np.dot(np.transpose(self.R_init_elbow), self.R_current_elbow)
        self.R_world2wrist = np.dot(np.transpose(self.R_init_wrist), self.R_current_wrist)
        self.R_elbow2wrist = np.dot(np.transpose(self.R_world2elbow), self.R_world2wrist)

        # Convert to Euler angles
        self.elbow_angles = m2e(self.R_world2elbow, axes="sxyz")
        self.wrist_angles = m2e(self.R_elbow2wrist, axes="sxyz")

        # update joint angles
        self.human_joint_info.position[0] = self.wrist_angles[0]
        self.human_joint_info.position[1] = self.wrist_angles[2]
        self.human_joint_info.position[2] = self.wrist_angles[1]
        self.human_joint_info.position[3] = self.elbow_angles[0]
        self.human_joint_info.position[4] = self.elbow_angles[2]
        self.human_joint_info.position[5] = self.elbow_angles[1]
