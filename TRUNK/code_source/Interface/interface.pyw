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
from error import Error

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

class Ui_MainWindow:
    def __init__(self,listRole,listIp,coach):
        self.coach = coach
        self.listRole = listRole
        self.listIp = listIp
        self.listIpConnected = []
        self.listRoleChoose = []
        self.app = QtGui.QApplication(sys.argv)
        self.MainWindow = QtGui.QMainWindow()
        self.setupUi()
        self.MainWindow.show()
        sys.exit(self.app.exec_())

    def setupUi(self):
        self.MainWindow.setObjectName(_fromUtf8("MainWindow"))
        self.MainWindow.resize(664, 600)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)

        self.centralwidget = QtGui.QWidget(self.MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 90, 591, 441))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

        self.vbox = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.vbox.setMargin(0)
        self.vbox.setObjectName(_fromUtf8("vbox"))

        self.listWidget = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget.setAlternatingRowColors(True)
        self.item = QtGui.QListWidgetItem(self.listWidget)
        self.listWidget.addItem(self.item)
        self.reference = MyCustomWidget("IP","Role",self.listWidget)
        self.item.setSizeHint(self.reference.minimumSizeHint())
        self.listWidget.setItemWidget(self.item,self.reference)

        self.vbox.addWidget(self.listWidget)

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.setObjectName(_fromUtf8("hbox"))

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem)

        self.addButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.addButton.setFont(self.font)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.hbox.addWidget(self.addButton)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem1)

        self.vbox.addLayout(self.hbox)

        self.exit = QtGui.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(550, 560, 75, 23))
        self.exit.setFont(self.font)
        self.exit.setObjectName(_fromUtf8("exit"))

        self.MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.MainWindow)
        self.eventUI()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.addButton.setText(_translate("MainWindow", "Add Robot", None))
        self.exit.setText(_translate("MainWindow", "Exit", None))

    def eventUI(self):
        self.exit.clicked.connect(self.close)
        self.addButton.clicked.connect(self.add)

    def close(self):
        self.coach.stopThreads()
        self.app.quit()

    def connectRobot(self,ip,role):
        self.ip = ip.encode('ascii','ignore')
        self.role = role.encode('ascii','ignore')

        if self.coach.createPlayer(self.ip,self.role):
            item = QtGui.QListWidgetItem(self.listWidget)
            self.listWidget.addItem(item)
            reference = MyCustomWidget(self.ip,self.role,self.listWidget)
            item.setSizeHint(reference.minimumSizeHint())
            self.listWidget.setItemWidget(item,reference)

            self.listIpConnected.append(self.ip)
            self.listIp.remove(self.ip)
            self.listRoleChoose.append(self.role)
            self.listRole.remove(self.role)
        else:
            # open the error window
            self.errorWindow()

    def add(self):
        self.addRobot = QtGui.QWidget()
        self.addRobotWindow = AddRobot()
        self.addRobotWindow.setupUi(self.addRobot,self.listIp,self.listRole)
        self.addRobot.setWindowModality(QtCore.Qt.ApplicationModal)
        self.MainWindow.connect(self.addRobot, SIGNAL("connection(PyQt_PyObject,PyQt_PyObject)"), self.connectRobot)
        self.addRobot.show()

    def errorWindow(self):
        self.error = QtGui.QWidget()
        self.errorWindow = Error()
        self.errorWindow.setupUi(self.error)
        self.error.setWindowModality(QtCore.Qt.ApplicationModal)
        self.error.show()


class MyCustomWidget(QtGui.QWidget):
    def __init__(self, ip, role, parent=None):
        super(MyCustomWidget, self).__init__(parent)

        self.row = QtGui.QHBoxLayout()

        self.row.addWidget(QtGui.QLabel(ip))
        self.row.addWidget(QtGui.QLabel(role))

        self.setLayout(self.row)


if __name__ == "__main__":
    listIp = ["127.0.0.1 ","172.96.26.32","172.96.26.33","172.96.26.34","172.96.26.35","172.96.26.36"]
    listRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
    ui = Ui_MainWindow(listRole,listIp)

