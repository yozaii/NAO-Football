import Interface.interface as interface
import Coach as coach

oumar = coach.Coach()
window = interface.Ui_MainWindow(oumar.get_listRole(),oumar.get_listIp(),oumar)