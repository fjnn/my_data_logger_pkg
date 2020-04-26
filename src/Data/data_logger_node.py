#!/usr/bin/env python

"""This is the script that works as a ROS node."""

import rospy
from Classes.IMU_subscriber_class import IMUdataRecorder
from Classes.UI_form import UI_form


if __name__ == "__main__":
    gui = UI_form()
    ros_node = IMUdataRecorder()
    while not rospy.is_shutdown():
        gui.update()
        ros_node.r.sleep()  # these lines are trivial at the moment. You need to implement these methods
