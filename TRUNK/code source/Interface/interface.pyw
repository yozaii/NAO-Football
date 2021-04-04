# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created: Sun Apr  4 20:03:04 2021
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
import sys
from addRobot import AddRobot

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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow,listRole,listIp):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(664, 600)
        self.MainWindow = MainWindow
        self.listRole = listRole
        self.listIp = listIp
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 90, 591, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.vbox = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.vbox.setMargin(0)
        self.vbox.setObjectName(_fromUtf8("vbox"))
        self.listWidget = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.vbox.addWidget(self.listWidget)
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.setObjectName(_fromUtf8("hbox"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem)
        self.addButton = QtGui.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addButton.setFont(font)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.hbox.addWidget(self.addButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem1)
        self.vbox.addLayout(self.hbox)
        self.exit = QtGui.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(550, 560, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.exit.setFont(font)
        self.exit.setObjectName(_fromUtf8("exit"))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.eventUI()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.addButton.setText(_translate("MainWindow", "Add Robot", None))
        self.exit.setText(_translate("MainWindow", "Exit", None))

    def eventUI(self):
        self.exit.clicked.connect(app.quit)
        self.addButton.clicked.connect(self.add)

    def test(self,ip,role):
        print "IP: ", ip
        print "Role: ",role

    def add(self):
        self.addRobot = QtGui.QWidget()
        self.ui = AddRobot()
        self.ui.setupUi(self.addRobot,self.listIp,self.listRole)
        self.addRobot.setWindowModality(QtCore.Qt.ApplicationModal)
        self.MainWindow.connect(self.addRobot, SIGNAL("connection(PyQt_PyObject,PyQt_PyObject)"), self.test)
        self.addRobot.show()

if __name__ == "__main__":
    listIp = ["127.0.0.1 ","172.96.26.32","172.96.26.33","172.96.26.34","172.96.26.35","172.96.26.36"]
    listRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,listRole,listIp)
    MainWindow.show()
    sys.exit(app.exec_())

