# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from subprocess import call
from modules.slideshow import Slides

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
        Form.resize(413, 300)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 30, 151, 51))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.checkBox = QtGui.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(210, 30, 99, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(260, 70, 68, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.figure = QtGui.QLabel(Form)
        self.figure.setGeometry(QtCore.QRect(30, 100, 51, 151))
        self.figure.setText(_fromUtf8(""))
        self.figure.setPixmap(QtGui.QPixmap(_fromUtf8("fig/skeleton-resizedWALK_0.png")))
        self.figure.setObjectName(_fromUtf8("figure"))
        self.textEdit = QtGui.QTextEdit(Form)
        self.textEdit.setGeometry(QtCore.QRect(100, 100, 301, 151))
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
        # self.slide()
        print "Logging started"
        # call(["rqt_plot"])  # here I will call my subscriber

    def slide(self, Form):
        # print "slide started"
        # self.image_files = image_files
        # self.timer = QtCore.QBasicTimer()
        # self.step = 0
        # self.delay = 500  # milliseconds
        # # self.timerEvent()
        # print "Slides are shown {} seconds apart".format(self.delay/1000.0)
        # print self.step
        # if self.step >= len(self.image_files):
        #     self.timer.stop()
        #     return
        # self.timer.start(self.delay, Form)
        # file = self.image_files[self.step]
        # image = QtGui.QPixmap(file)
        # self.figure.setPixmap(image)
        # self.step += 1
        # print self.step
        self.image_files = image_files
        self.label = QtGui.QLabel(s, self)
        self.label.setGeometry(10, 30, 640, 480)
        self.button = QtGui.QPushButton("Start Slide Show",self)
        self.button.setGeometry(10, 10, 140, 30)
        self.button.clicked.connect(self.timerEvent)
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 500  # milliseconds
        sf = "Slides are shown {} seconds apart"
        self.setWindowTitle(sf.format(self.delay/1000.0))


    def timerEvent(self, Form):
        if self.step >= len(self.image_files):
            self.timer.stop()
            self.button.setText('Slide Show Finished')
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        image = QtGui.QPixmap(file)
        self.label.setPixmap(image)
        self.setWindowTitle("{} --> {}".format(str(self.step), file))
        self.step += 1

    def message(self):
	print "Sondre <3 Gizem"


image_files = [
    "fig/skeleton-resizedWALK_0",
    "fig/skeleton-resizedWALK_1",
    "fig/skeleton-resizedWALK_2",
    "fig/skeleton-resizedWALK_3",
    "fig/skeleton-resizedWALK_4"
]

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    ui.slide(Form)
    # pitchSlide = Slides(image_files=image_files)
    Form.show()
    sys.exit(app.exec_())
