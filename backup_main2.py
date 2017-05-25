import sys
import os
from PyQt4 import QtCore, QtGui, QtSql, uic
import database
import time
from sensor import run

qtCreatorFile = "main2.ui" # Enter file here.

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

global flag
flag = 0

class ServerThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)

    def start_server(self):
        x=0
        while True:
            time.sleep(1)
            os.system('python sensor.py')
            ketinggian = run(self)
            #print('nilai i = %d' % ketinggian)
            if (x==0):
                b = ketinggian
                x+=1
            elif (x==9):
                percepatan = abs(ketinggian - b)
                print("percepatan = {0}".format(percepatan))
                self.emit(QtCore.SIGNAL("cepat(float)"), float(percepatan))
                x = 0
            else:
                x+=1
            self.emit(QtCore.SIGNAL("tinggi(float)"), float(ketinggian))
    
    def run(self):
        self.start_server()

class SmsDangerThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)

    def start_server(self):
        query = QtSql.QSqlQuery("SELECT nohp  FROM data_diri")
        while(query.next()):
            nope = str(query.value(0)) #di Windows gk prlu dtmbahkan .toString()
            print("Sungai dalam keadaan Bahaya : {0}".format(nope))
            #os.system('echo "Sungai keadaan BAHAYA" | sudo gammu sendsms TEXT {0}'.format(nope))
    
    def run(self):
        self.start_server()

class SmsWarningThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)

    def start_server(self):
        query = QtSql.QSqlQuery("SELECT nohp  FROM data_diri")
        while(query.next()):
            nope = str(query.value(0)) #di Windows gk prlu dtmbahkan .toString()
            print("Sungai dalam keadaan Warning : {0}".format(nope))
            #os.system('echo "Sungai keadaan Warning" | sudo gammu sendsms TEXT {0}'.format(nope))
    
    def run(self):
        self.start_server()

class MyApp(QtGui.QMainWindow, Ui_MainWindow, QtGui.QWidget):

    def __init__(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('data.db')
        open = self.db.open()
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
        
        self.dan = QtGui.QCheckBox(self.danger)
        self.war = QtGui.QCheckBox(self.warning)
        self.ama = QtGui.QCheckBox(self.aman)

        self.thread = ServerThread()
        self.thread.start()
        self.connect(self.thread, QtCore.SIGNAL("tinggi(float)"), self.tinggi)
        self.connect(self.thread, QtCore.SIGNAL("cepat(float)"), self.cepat)

    def tinggi(self,a):
        self.ketinggian.display(a)
    
    def cepat(self,a):
        self.percepatan.display(a)

    def doing(self, a):
        self.hasil.display(a)
        if float(a) < 10.0:
            self.dan.setChecked(True)
            self.war.setChecked(False)
            self.ama.setChecked(False)
            x = 1
            self.sendsms(x)
        elif 10.0 <= float(a) < 20.0:
            self.dan.setChecked(False)
            self.war.setChecked(True)
            self.ama.setChecked(False)
            x = 2
            self.sendsms(x)
        else :
            self.dan.setChecked(False)
            self.war.setChecked(False)
            self.ama.setChecked(True)
            x = 3
            self.sendsms(x)
    
    def sendsms(self,x):
        global flag
        temp = x
        b = flag
        flag = temp
        if(x!=b):
            if(x==1) :
                self.thread1 = SmsDangerThread()
                self.thread1.start()
            elif(x==2):
                self.thread2 = SmsWarningThread()
                self.thread2.start()

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
