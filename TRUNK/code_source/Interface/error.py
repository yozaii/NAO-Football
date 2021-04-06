# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'error.ui'
#
# Created: Mon Apr  5 18:43:30 2021
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys,os
from pathlib2 import Path

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

class Error(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(475, 148)
        directory = Path(__file__).parent
        self.pixmap = QtGui.QPixmap(str(directory)+"\error.png")
        if self.pixmap.isNull():
            print "error pictures"

        self.pic = QtGui.QLabel(Form)
        self.pic.setGeometry(QtCore.QRect(20, 30, 81, 81))
        self.pic.setSizeIncrement(QtCore.QSize(10, 10))
        self.pic.setPixmap(self.pixmap)
        self.pic.setScaledContents(True)
        self.pic.setObjectName(_fromUtf8("pic"))

        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 30, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(170, 70, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Error", None))
        self.label.setText(_translate("Form", "Error: we can\'t connect to the NAO proxy.", None))
        self.label_3.setText(_translate("Form", " Please check the Robot is switched on", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Error()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

