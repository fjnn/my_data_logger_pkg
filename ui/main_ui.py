# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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
        self.figure.setPixmap(QtGui.QPixmap(_fromUtf8("fig/ball/pitch/p0.png")))
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
        print "Logging started"
        self.textEdit.setText("Logging started")

        self.textEdit.append("VERTICAL motion in 2 sec")
        mainTimer.start(2000)
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
            self.figure.setPixmap(QtGui.QPixmap(_fromUtf8("fig/ball/"+motion+str(pic_list[pic_index])+".png")))
            pic_index += 1
        else:
            pic_index = 0
            self.textEdit.append(motion_text)
            mainTimer.start(2000)
            self.figure.setPixmap(QtGui.QPixmap(_fromUtf8("fig/ball/"+motion+str(pic_list[pic_index])+".png")))
            motion_index += 1


if __name__ == "__main__":
    import sys
    import roslaunch
    package = 'rqt_gui'
    executable = 'rqt_gui'
    node = roslaunch.core.Node(package, executable)
    launch = roslaunch.scriptapi.ROSLaunch()
    launch.start()

    process = launch.launch(node)
    print process.is_alive()
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
    secondTimer = QtCore.QTimer()
    mainTimer.timeout.connect(ui.show_next_pic)  # neden show_next_pic() deyince hatali? Cunku func cagirmiyoruz, onunla bagliyoruz.
    sys.exit(app.exec_())
