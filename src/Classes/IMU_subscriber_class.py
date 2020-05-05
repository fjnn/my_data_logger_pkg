#!/usr/bin/env python

"""
This is a subscriber. Subscribes the IMU readings and save into data_logger_module.

"""

# TODO: Elbow ve Wrist IMU ayni time frame'de aldigina emin ol.

# imports
import Data.data_logger_module as data_logger

import rospy
import numpy as np
from sensor_msgs.msg import JointState
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_matrix as q2m
from tf.transformations import euler_from_matrix as m2e

_CALIBRATION_TH = 60


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
        self.wrist_angles_rpy = Vector3()
        self.human_joint_info = JointState()
        self.human_joint_info.name = ['human_wrist_pitch', 'human_wrist_roll', 'human_wrist_yaw', 'human_elbow_pitch', 'human_elbow_roll', 'human_elbow_yaw']
        self.human_joint_info.position = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.calibration_flag = 0
        # self.IMU_init = {"quat_pose_elbow": [0.0, 0.0, 0.0, 0.0], "quat_pose_wrist": [0.0, 0.0, 0.0, 0.0]}
        self.quat_pose_elbow_init = Quaternion()
        self.quat_pose_wrist_init = Quaternion()
        self.runflag = False

        print "Initialized"

    def init_subscribers_and_publishers(self):
        self.pub = rospy.Publisher('/joint_states', JointState, queue_size=1)
        self.pub_wrist_angles = rospy.Publisher('/wrist_angles_rpy', Vector3, queue_size=1)
        self.sub_imu_e = rospy.Subscriber('/sensor_l_elbow', Imu, self.cb_imu_elbow)
        self.sub_imu_w = rospy.Subscriber('/sensor_l_wrist', Imu, self.cb_imu_wrist)
        self.log_start_time = rospy.get_time()
        self.data_logger_enabler()
        self.runflag = True

    def data_logger_enabler(self):
        print "enable_logging"
        data_logger.enable_logging()

    def update(self):
        print self.calibration_flag
        self.human_joint_info.header.stamp = rospy.Time.now()
        # data_logger.log_metrics(tg=rospy.get_time(), te=rospy.get_time()-self.log_start_time, pitch=self.human_joint_info.position[0], roll=self.human_joint_info.position[1], yaw=self.human_joint_info.position[2], mark="not-aided")
        self.calibration_flag = self.calibration_flag + 1
        self.pub.publish(self.human_joint_info)
        self.wrist_angles_rpy.x = np.degrees(self.human_joint_info.position[0])  # pitch
        self.wrist_angles_rpy.y = np.degrees(self.human_joint_info.position[1])  # yaw
        self.wrist_angles_rpy.z = np.degrees(self.human_joint_info.position[2])  # roll
        self.pub_wrist_angles.publish(self.wrist_angles_rpy)

    def cb_imu_elbow(self, msg):
        self.elbow_measurement = msg
        while self.calibration_flag < _CALIBRATION_TH:
            self.quat_pose_elbow_init = self.elbow_measurement.orientation
            print "calibrating"
        # Initial measurements for calibration
        self.R_init_elbow = q2m([self.quat_pose_elbow_init.x, self.quat_pose_elbow_init.y, self.quat_pose_elbow_init.z, self.quat_pose_elbow_init.w])
        # Current Measurements
        self.R_current_elbow = q2m([self.elbow_measurement.orientation.x, self.elbow_measurement.orientation.y, self.elbow_measurement.orientation.z, self.elbow_measurement.orientation.w])
        # Rotation matrices
        self.R_world2elbow = np.dot(np.transpose(self.R_init_elbow), self.R_current_elbow)
        # Convert to Euler angles
        self.elbow_angles = m2e(self.R_world2elbow, axes="sxyz")
        # Update joint angles
        self.human_joint_info.position[3] = self.elbow_angles[0]
        self.human_joint_info.position[4] = self.elbow_angles[2]
        self.human_joint_info.position[5] = self.elbow_angles[1]

    def cb_imu_wrist(self, msg):
        self.wrist_measurement = msg
        while self.calibration_flag < _CALIBRATION_TH:
            self.quat_pose_wrist_init = self.wrist_measurement.orientation
        # Initial measurements for calibration
        self.R_init_wrist = q2m([self.quat_pose_wrist_init.x, self.quat_pose_wrist_init.y, self.quat_pose_wrist_init.z, self.quat_pose_wrist_init.w])
        # Current Measurements
        self.R_current_wrist = q2m([self.wrist_measurement.orientation.x, self.wrist_measurement.orientation.y, self.wrist_measurement.orientation.z, self.wrist_measurement.orientation.w])
        # Rotation matrices
        self.R_world2wrist = np.dot(np.transpose(self.R_init_wrist), self.R_current_wrist)
        self.R_elbow2wrist = np.dot(np.transpose(self.R_world2elbow), self.R_world2wrist)
        # Convert to Euler angles
        self.wrist_angles = m2e(self.R_elbow2wrist, axes="sxyz")
        # update joint angles
        self.human_joint_info.position[0] = self.wrist_angles[0]
        self.human_joint_info.position[1] = self.wrist_angles[2]
        self.human_joint_info.position[2] = self.wrist_angles[1]
