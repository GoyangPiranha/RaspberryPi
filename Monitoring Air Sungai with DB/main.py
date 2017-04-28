import sys
from PyQt4 import QtCore, QtGui, QtSql, uic
import database

qtCreatorFile = "main.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow, QtGui.QWidget):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)  
        self.tampilkan()
        self.del_btn.clicked.connect(lambda: self.tw.removeRow(self.tw.currentIndex().row()))
    
    def tampilkan(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data.db')
        open = db.open()
        self.tw.setColumnCount(3)
        self.tw.setHorizontalHeaderLabels(['ID','NAMA','NO HP'])
        row = 0
        sql = "SELECT * FROM data_diri"
        query = QtSql.QSqlQuery(sql)
        while query.next():
            self.tw.insertRow(row)
            id = QtGui.QTableWidgetItem(str(query.value(0)))
            nama = QtGui.QTableWidgetItem(str(query.value(1)))
            nohp = QtGui.QTableWidgetItem(str(query.value(2)))
            self.tw.setItem(row, 0, id)
            self.tw.setItem(row, 1, nama)
            self.tw.setItem(row, 2, nohp)
            row = row + 1
        db.close()

def findrow(self):
    delrow = i.row()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
