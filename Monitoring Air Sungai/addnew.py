from __future__ import division
import sys
import csv
from PyQt4 import QtCore, QtGui, uic

qtCreatorFile = "add.ui" # Enter file here.

Ui_AddWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyAppadd(QtGui.QMainWindow, Ui_AddWindow, QtGui.QWidget):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_AddWindow.__init__(self)
        self.setupUi(self)
        self.add.clicked.connect(self.tambah)
        
    def tambah(self):
        namax = str(self.nama.toPlainText())
        petik = "\""
        petik1= '"'
        name = petik1 + namax
        nohpx = str(self.nohp.toPlainText())
        nohp = nohpx + petik
        databaru = [[name, nohp]]
        with open('data.csv', 'a', newline='') as filecsv:
            datafile = csv.writer(filecsv)
            datafile.writerows(databaru)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyAppadd()
    window.show()
    sys.exit(app.exec_())
