# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

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

class AddRobot(object):
    def setupUi(self, addRobot,listIp,listRole):

        self.addRobot = addRobot
        # window initalisation
        self.addRobot.setObjectName(_fromUtf8("addRobot"))
        self.addRobot.resize(360, 144)

        self.font = QtGui.QFont()
        self.font.setPointSize(12)

        self.verticalLayoutWidget = QtGui.QWidget(addRobot)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(5, 2, 350, 142))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))

        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.labelRobotIp = QtGui.QLabel(self.verticalLayoutWidget)
        
        self.labelRobotIp.setFont(self.font)
        self.labelRobotIp.setObjectName(_fromUtf8("labelRobotIp"))
        self.horizontalLayout.addWidget(self.labelRobotIp)

        self.boxIp = QtGui.QComboBox(self.verticalLayoutWidget)
        self.boxIp.setFont(self.font)
        self.boxIp.setObjectName(_fromUtf8("boxIp"))
        self.boxIp.addItems(listIp)
        self.horizontalLayout.addWidget(self.boxIp)

        self.labelRole = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelRole.setFont(self.font)
        self.labelRole.setObjectName(_fromUtf8("labelRole"))
        self.horizontalLayout.addWidget(self.labelRole)

        self.boxRole = QtGui.QComboBox(self.verticalLayoutWidget)
        self.boxRole.setFont(self.font)
        self.boxRole.setObjectName(_fromUtf8("boxRole"))
        self.boxRole.addItems(listRole)
        self.horizontalLayout.addWidget(self.boxRole)

        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))


        self.labelAdd = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelAdd.setFont(self.font)
        self.labelAdd.setObjectName(_fromUtf8("labelAdd"))
        self.horizontalLayout_2.addWidget(self.labelAdd)

        self.addButton = QtGui.QPushButton(self.verticalLayoutWidget)
        self.addButton.setFont(self.font)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.horizontalLayout_2.addWidget(self.addButton)

        spacerItem = QtGui.QSpacerItem(100, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.exit = QtGui.QPushButton(self.verticalLayoutWidget)
        self.exit.setFont(self.font)
        self.exit.setObjectName(_fromUtf8("exit"))
        self.horizontalLayout_2.addWidget(self.exit)

        spacerItem2 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(addRobot)
        self.eventUI()
        QtCore.QMetaObject.connectSlotsByName(addRobot)

    def retranslateUi(self,addRobot):
        addRobot.setWindowTitle(_translate("addRobot", "addRobot", None))
        self.labelRobotIp.setText(_translate("addRobot", "Robot IP", None))
        self.labelRole.setText(_translate("addRobot", "Role", None))
        self.labelAdd.setText(_translate("addRobot", "Add robot", None))
        self.addButton.setText(_translate("addRobot", "connect", None))
        self.exit.setText(_translate("Form", "cancel", None))

    def add(self):
        self.addRobot.close()
        self.addRobot.emit(SIGNAL("connection(PyQt_PyObject,PyQt_PyObject)"), unicode(self.boxIp.currentText()),unicode(self.boxRole.currentText()))

    def eventUI(self):
        self.addButton.clicked.connect(self.add)
        self.exit.clicked.connect(self.close)
    
    def close(self):
        self.addRobot.close()

#******************     TEST addRobot    *********************#

if __name__ == "__main__":
    import sys
    
    listIp = ["172.96.26.32","172.96.26.33","172.96.26.34","172.96.26.35","172.96.26.36"]
    listRole = ["GOAL","RDEFENSE","LDEFENSE","RATTACKER","LATTACKER","MIDDLE"]
    app = QtGui.QApplication(sys.argv)
    addRobot = QtGui.QWidget()
    ui = AddRobot()
    ui.setupUi(addRobot,listIp,listRole)
    addRobot.show()
    sys.exit(app.exec_())
    
