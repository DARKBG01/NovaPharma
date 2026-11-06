from PySide6 import QtCore



class Worker(QtCore.QThread):
    finished = QtCore.Signal(str)

    def run(self):
        result = "Terminé"
        self.finished.emit(result)