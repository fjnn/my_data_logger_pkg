#!/usr/bin/env python3
''' ps_Image_slides101.py
A simple slide show using PySide (PyQT)
PySide is the official LGPL-licensed version of PyQT
I downloaded and used the Windows self-extracting installers
for Python27:
PySide-1.2.1.win32-py2.7.exe
for Python33:
PySide-1.2.1.win32-py3.3.exe
from:
http://qt-project.org/wiki/PySide_Binaries_Windows
tested with PySide121 and Python27/33  by  vegaseat  18nov2013

from PySide.QtCore import *
from PySide.QtGui import *

'''
from PyQt4 import QtCore, QtGui


class Slides(QtGui.QWidget):
    def __init__(self, image_files, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.image_files = image_files
        self.timer = QtCore.QBasicTimer()
        self.step = 0
        self.delay = 500  # milliseconds
        self.timerEvent(parent)
        print "Slides are shown {} seconds apart".format(self.delay/1000.0)  # TODO: check old code. make it fancy

    def timerEvent(self, parent=None, e=None):
        if self.step >= len(self.image_files):
            self.timer.stop()
            return
        self.timer.start(self.delay, self)
        file = self.image_files[self.step]
        image = QtGui.QPixmap(file)
        # parent.label.setPixmap(image)
        self.step += 1
