import sys
from PyQt5.QtWidgets import QApplication, QWidget

 
class window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Coach Interface")
        self.resize(1000,700)

app = QApplication.instance()
if not app: 
    app = QApplication(sys.argv)

window = Window()
window.show()

app.exec_()