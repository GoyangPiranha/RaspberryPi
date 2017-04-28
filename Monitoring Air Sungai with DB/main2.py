import sys
from PyQt4 import QtCore, QtGui, QtSql, uic
import database

qtCreatorFile = "main.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtGui.QMainWindow, Ui_MainWindow, QtGui.QWidget):

    def __init__(self):
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('data.db')
        open = db.open()
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)  

        self.model = QtSql.QSqlTableModel()
        delrow = -1
        self.initializeModel(self.model)
        
        view1 = self.createView(self.model)
        view1.clicked.connect(findrow)

        self.del_btn.clicked.connect(lambda: self.model.removeRow(view1.currentIndex().row()))
        self.add_btn.clicked.connect(self.addrow)

    def createView(self, model):
        self.tw.setModel(model)
        return self.tw

    def initializeModel(self, model):
        model.setTable('data_diri')
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        model.setHeaderData(1, QtCore.Qt.Horizontal, "Nama")
        model.setHeaderData(2, QtCore.Qt.Horizontal, "No HP")

    def addrow(self):
        ret = self.model.insertRows(self.model.rowCount(), 1)

def findrow(i):
    delrow = i.row()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
