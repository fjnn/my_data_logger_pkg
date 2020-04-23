#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is a subscriber. Subscribes the IMU readings and save by data_logger_module.
Also it creates the gui using PyQt4.

#TODO: Seperate class into a different file.

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

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

figures_path = "../ui/fig/ball/"


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(562, 384)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 30, 151, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(210, 30, 99, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(380, 80, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.figure = QtGui.QLabel(Form)
        self.figure.setGeometry(QtCore.QRect(20, 100, 271, 281))
        self.figure.setText(_fromUtf8(""))
        self.figure.setPixmap(QtGui.QPixmap(_fromUtf8(figures_path+"pitch/p0.png")))
        self.figure.setObjectName(_fromUtf8("figure"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(290, 110, 261, 261))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), self.start_logging)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton.setText(_translate("Form", "Start", None))
        self.checkBox.setText(_translate("Form", "logging", None))
        self.label.setText(_translate("Form", "Progress", None))

    def start_logging(self):
        """This func is connected to the start button"""
        rosnode()
        print "Logging started"
        self.textEdit.setText("Logging started")
        self.textEdit.append("VERTICAL motion in 2 sec")
        mainTimer.start(2000)
        secondTimer.start(100)
        # call(["rqt_plot"])  # here I will call my subscriber

    def show_next_pic(self):
        """ Returns one pic every time tick.
            Ps: For loops don't work"""
        global pic_index, motion_index
        # self.textEdit.append(str(motion_index)+"-"+str(pic_index))
        if motion_index == 0:  # pitch
            motion = "pitch/p"
            motion_text = "HORIZONTAL motion in 2 sec"
        elif motion_index == 1:  # yaw
            motion = "yaw/y"
            motion_text = "ROTATIONAL motion in 2 sec"
        elif motion_index == 2:
            motion = "roll/r"
            motion_text = "Simulation is completed"
        else:
            print "Simulation is over"
            motion_text = "error"
            mainTimer.stop()
            # sys.exit(app.exec_())

        if pic_index <= 23:
            mainTimer.start(300)
            self.figure.setPixmap(QtGui.QPixmap(_fromUtf8(figures_path+motion+str(pic_list[pic_index])+".png")))
            pic_index += 1
        else:
            pic_index = 0
            self.textEdit.append(motion_text)
            mainTimer.start(2000)
            self.figure.setPixmap(QtGui.QPixmap(_fromUtf8(figures_path+motion+str(pic_list[pic_index])+".png")))
            motion_index += 1

    def message(self):
        print "Sondre <3 Gizem"


rospy.init_node('data_logger_sub')

# variable definitions
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
        # print "calibrating"

    R_init_wrist = q2m([IMU_init["quat_pose_wrist"].x, IMU_init["quat_pose_wrist"].y, IMU_init["quat_pose_wrist"].z, IMU_init["quat_pose_wrist"].w])
    R_current_wrist = q2m([msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w])
    R_world2wrist = np.dot(np.transpose(R_init_wrist), R_current_wrist)
    R_elbow2wrist = np.dot(np.transpose(R_world2elbow), R_world2wrist)

    wrist_angles = m2e(R_elbow2wrist, axes="sxyz")
    # print "%5.2f --- %5.2f -- %5.2f" % wrist_angles

    human_joint_info.position[0] = wrist_angles[0]
    human_joint_info.position[1] = wrist_angles[2]
    human_joint_info.position[2] = wrist_angles[1]


def rosnode():
    global joint_info, calibration_flag
    initial_flag = True

    if not initial_flag:
        pub = rospy.Publisher('/joint_states', JointState, queue_size=1)
        sub_imu_e = rospy.Subscriber('/sensor_l_elbow', Imu, callback_imu_elbow)
        sub_imu_w = rospy.Subscriber('/sensor_l_wrist', Imu, callback_imu_wrist)
        data_logger.enable_logging()
        rate = rospy.Rate(10)
        log_start_time = rospy.get_time()
    else:
        human_joint_info.header.stamp = rospy.Time.now()
        data_logger.log_metrics(tg=rospy.get_time(), te=rospy.get_time()-log_start_time, pitch=human_joint_info.position[0], roll=human_joint_info.position[1], yaw=human_joint_info.position[2], mark="not-aided")
        calibration_flag = calibration_flag + 1
        pub.publish(human_joint_info)
        rate.sleep()


if __name__ == '__main__':
    import sys
    pic_list = [0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1,
                0, 7, 8, 9, 10, 11, 12, 11, 10, 9, 8, 7]
    pic_index = 0
    motion_index = 0
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    mainTimer = QtCore.QTimer()
    mainTimer.timeout.connect(ui.show_next_pic)  # neden show_next_pic() deyince hatali? Cunku func cagirmiyoruz, onunla bagliyoruz.
    initial_flag = False
    secondTimer = QtCore.QTimer()
    secondTimer.timeout.connect(rosnode)
    # secondTimer = QtCore.QTimer()
    # secondTimer.timeout.connect(ui.rosnode)
    sys.exit(app.exec_())
