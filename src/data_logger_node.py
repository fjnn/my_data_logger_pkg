#!/usr/bin/env python

"""This is the script that works as a ROS node.
    No need any longer
    Keep it as test"""

import rospy
from Classes.IMU_subscriber_class import IMUdataRecorder
# from Classes.UI_form import UI_form


if __name__ == "__main__":
    ros_node = IMUdataRecorder()
    while not ros_node.runflag:
        ros_node.update()
