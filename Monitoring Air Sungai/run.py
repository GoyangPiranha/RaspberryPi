from __future__ import division
import sys
import csv
from PyQt4 import QtCore, QtGui, uic
from addnew import Ui_AddWindow

qtCreatorFile = "kontak.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow, QtGui.QWidget):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.refresh.clicked.connect(self.tampilkan)
        self.add.clicked.connect(self.tambah)
        #self.del.clicked.connect(self.hapus)
        #self.edit.clicked.connect(self.ubah)
    
    def tampilkan(self):
        with open('data.csv', 'r') as filecsv:
            datafile = csv.reader(filecsv)
            fx_elements = {}
            for row in datafile:
                key = row[0]
                if key in fx_elements:
                    pass
                fx_elements[key] = row[1:]
            list = sorted(fx_elements.keys())
            for k in list:
                item = QtGui.QListWidgetItem(k)
                self.hasil.addItem(item)
        
    def tambah(self):
        self.addwindow = QtGui.QMainWindow()
        self.ui = Ui_AddWindow()
        self.ui.setupUi(self.addwindow)
        self.addwindow.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
