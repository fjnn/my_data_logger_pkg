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

# TO RUN MANUAL
# if __name__ == "__main__":
#     ros_node = IMUdataRecorder()
#     ros_node.init_subscribers_and_publishers()
#     # while not ros_node.runflag:
#     while not rospy.is_shutdown():
#         ros_node.update()
