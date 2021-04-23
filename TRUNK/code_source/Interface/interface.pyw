# -*- coding: utf-8 -*-

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
        self.MainWindow.resize(660, 600)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)



        # principal window
        self.centralwidget = QtGui.QWidget(self.MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # principal vbox
        self.verticalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 55, 591, 480))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.vbox = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.vbox.setMargin(0)
        self.vbox.setObjectName(_fromUtf8("vbox"))

        # first hbox with kickoff button and timer
        self.hbox1 = QtGui.QHBoxLayout()
        self.hbox1.setMargin(0)
        self.hbox1.setObjectName(_fromUtf8("hbox1"))

        self.kickOffButton = QtGui.QRadioButton(self.verticalLayoutWidget)
        self.kickOffButton.setEnabled(True)
        self.kickOffButton.setFont(self.font)
        self.kickOffButton.setObjectName(_fromUtf8("kickOffButton"))
        self.hbox1.addWidget(self.kickOffButton)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox1.addItem(spacerItem1)

        self.vbox1 = QtGui.QVBoxLayout()
        self.vbox1.setObjectName(_fromUtf8("vbox1"))

        self.time = QtGui.QLabel(self.verticalLayoutWidget)
        self.time.setFont(self.font)
        self.time.setObjectName(_fromUtf8("time"))
        self.vbox1.addWidget(self.time)

        self.hbox2 = QtGui.QHBoxLayout()
        self.hbox2.setMargin(0)
        self.hbox2.setObjectName(_fromUtf8("hbox2"))

        self.startButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.startButton.setFont(self.font)
        self.startButton.setObjectName(_fromUtf8("startButton"))

        self.stopButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.stopButton.setFont(self.font)
        self.stopButton.setObjectName(_fromUtf8("stopButton"))

        self.resetButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.resetButton.setFont(self.font)
        self.resetButton.setObjectName(_fromUtf8("resetButton"))

        self.hbox2.addWidget(self.startButton)
        self.hbox2.addWidget(self.stopButton)
        self.hbox2.addWidget(self.resetButton)

        self.vbox1.addLayout(self.hbox2)

        self.hbox1.addLayout(self.vbox1)

        self.vbox.addLayout(self.hbox1)

        # list of robot

        self.listWidget = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.listWidget.setAlternatingRowColors(True)

        self.item = QtGui.QListWidgetItem(self.listWidget)
        self.listWidget.addItem(self.item)
        self.reference = MyCustomWidget("IP","Role",self.listWidget)
        self.item.setSizeHint(self.reference.minimumSizeHint())
        self.listWidget.setItemWidget(self.item,self.reference)

        self.vbox.addWidget(self.listWidget)


        # button add ready disconnect

        self.hbox = QtGui.QHBoxLayout()
        self.hbox.setObjectName(_fromUtf8("hbox"))

        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem)

        self.addButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.addButton.setFont(self.font)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.hbox.addWidget(self.addButton)

        self.readyButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.readyButton.setFont(self.font)
        self.readyButton.setObjectName(_fromUtf8("readyButton"))
        self.hbox.addWidget(self.readyButton)

        self.disconnectButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.disconnectButton.setFont(self.font)
        self.disconnectButton.setObjectName(_fromUtf8("disconnectButton"))
        self.hbox.addWidget(self.disconnectButton)

        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hbox.addItem(spacerItem1)

        self.vbox.addLayout(self.hbox)

        # exit button

        self.exit = QtGui.QPushButton(self.centralwidget)
        self.exit.setGeometry(QtCore.QRect(550, 560, 75, 23))
        self.exit.setFont(self.font)
        self.exit.setObjectName(_fromUtf8("exit"))

        self.MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(self.MainWindow)
        self.eventUI()
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Robot Interface", None))
        self.addButton.setText(_translate("MainWindow", "Add Robot", None))
        self.readyButton.setText(_translate("MainWindow", "Ready", None))
        self.disconnectButton.setText(_translate("MainWindow", "Disconnect", None))
        self.exit.setText(_translate("MainWindow", "Exit", None))
        self.kickOffButton.setText(_translate("MainWindow", "Kickoff", None))
        self.time.setText(_translate("MainWindow", "Time: "+ str(self.coach.timer.minute) +":"+str(self.coach.timer.sec), None))
        self.startButton.setText(_translate("MainWindow", "Start", None))
        self.stopButton.setText(_translate("MainWindow", "Stop", None))
        self.resetButton.setText(_translate("MainWindow", "Reset", None))

    def eventUI(self):
        """
        contains all of the widget event
        """
        self.exit.clicked.connect(self.close)
        self.addButton.clicked.connect(self.add)
        self.readyButton.clicked.connect(self.takeReady)
        self.disconnectButton.clicked.connect(self.disconnect)
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.resetButton.clicked.connect(self.reset)
        self.kickOffButton.clicked.connect(self.kickoffIsOn)

    def start(self):
        """
        start the timer
        """
        self.coach.timer.setup(self)
        self.coach.timer.start()

    def stop(self):
        """
        stop the timer
        """
        self.coach.timer.stop()

    def reset(self):
        """
        reset the timer
        """
        self.coach.timer.reset()

    def close(self):
        """
        stop all threads
        """
        self.coach.stopThreads()
        self.app.quit()

    def connectRobot(self,ip,role):
        """
        allows to ask the connection and update view
        """
        self.ip = ip.encode('ascii','ignore')
        self.role = role.encode('ascii','ignore')

        # verify if the connection are allowed
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
        """
        display the window who allows to add robot
        """
        self.addRobot = QtGui.QWidget()
        self.addRobotWindow = AddRobot()
        self.addRobotWindow.setupUi(self.addRobot,self.listIp,self.listRole)
        self.addRobot.setWindowModality(QtCore.Qt.ApplicationModal)
        self.MainWindow.connect(self.addRobot, SIGNAL("connection(PyQt_PyObject,PyQt_PyObject)"), self.connectRobot)
        self.addRobot.show()

    def errorWindow(self):
        """
        display the error window
        """
        self.error = QtGui.QWidget()
        errorWindow = Error()
        errorWindow.setupUi(self.error)
        self.error.setWindowModality(QtCore.Qt.ApplicationModal)
        self.error.show()

    def disconnect(self):
        """
        ask to disconnect a robot
        """
        qWidget = self.listWidget.itemWidget(self.listWidget.currentItem())
        selectedIp = qWidget.ip
        selectedRole = qWidget.role
        if self.coach.stopThread(selectedIp):
            self.listIpConnected.remove(selectedIp)
            self.listIp.append(selectedIp)
            self.listRoleChoose.remove(selectedRole)
            self.listRole.append(selectedRole)
            self.listWidget.removeItemWidget(self.listWidget.currentItem())

    def kickoffIsOn(self):
        """
        change the kickoff variable
        """
        if self.kickOffButton.isChecked():
            
            self.coach.kickoff = True
        else:
            self.coach.kickoff = False

    def takeReady(self):
        """
        change states of robot to be ready
        """
        self.coach.ready()

class MyCustomWidget(QtGui.QWidget):
    """
    Custom widget to list ip and role
    """
    def __init__(self, ip, role, parent=None):
        super(MyCustomWidget, self).__init__(parent)
        self.ip = ip
        self.role = role
        self.row = QtGui.QHBoxLayout()
        self.row.addWidget(QtGui.QLabel(self.ip))
        self.row.addWidget(QtGui.QLabel(role))
        self.setLayout(self.row)

#******************     TEST Interface    *********************#

if __name__ == "__main__":
    import Coach as coach
    listIp = ["127.0.0.1 ","172.96.26.32","172.96.26.33","172.96.26.34","172.96.26.35","172.96.26.36"]
    listRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
    ui = Ui_MainWindow(listRole,listIp,coach.Coach())

