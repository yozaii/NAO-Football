import sys
from PyQt5.QtWidgets import QApplication, QWidget

app = QApplication.instance() 
if not app: 
    app = QApplication(sys.argv)


window = QWidget()
window.setWindowTitle("Coach Interface")
window.resize(1000,700)


window.show()

app.exec_()