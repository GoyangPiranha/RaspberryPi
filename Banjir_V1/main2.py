import sys
import os
from PyQt4 import QtCore, QtGui, QtSql, uic
import database
import time
from dummy import run
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

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
            os.system('python dummy.py')
            ketinggian = run(self)
            #print("Ketinggian : {0}".format(ketinggian))

            if (x==0):
                b = ketinggian
                x+=1
            elif (x==9):
                percepatan = abs(ketinggian - b)
                #print("Percepatan : {0}".format(percepatan))
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

class FuzzyThread(QtCore.QThread):
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self)
        # New Antecedent/Consequent objects hold universe variables and membership # functions 
        x_ketinggian = ctrl.Antecedent(np.arange(0, 20, 1), 'ketinggian')
        x_percepatan = ctrl.Antecedent(np.arange(0, 20, 1), 'percepatan') 
        x_status = ctrl.Consequent(np.arange(0, 20, 1), 'status')

        # Custom membership functions can be built interactively with a familiar, # Pythonic API 
        x_ketinggian['tinggi'] = fuzz.trapmf(x_ketinggian.universe, [0, 0, 10, 10]) 
        x_ketinggian['sedang'] = fuzz.trimf(x_ketinggian.universe, [10, 14, 18]) 
        x_ketinggian['rendah'] = fuzz.trapmf(x_ketinggian.universe, [14, 18, 20, 20])

        x_percepatan['lamban'] = fuzz.trapmf(x_percepatan.universe, [0, 0, 2, 4]) 
        x_percepatan['sedang'] = fuzz.trimf(x_percepatan.universe, [2, 4, 6]) 
        x_percepatan['cepat'] = fuzz.trapmf(x_percepatan.universe, [4, 6, 10, 20])

        x_status['bahaya'] = fuzz.trapmf(x_status.universe, [0, 0, 10, 10]) 
        x_status['siaga'] = fuzz.trimf(x_status.universe, [10, 14, 18]) 
        x_status['aman'] = fuzz.trapmf(x_status.universe, [14, 18, 20, 20])

        # You can see how these look with .view()
        #x_ketinggian.view()

        #x_percepatan.view()

        #x_status.view()

        rule1 = ctrl.Rule(x_ketinggian['rendah'] & x_percepatan['lamban'], x_status['aman'])
        rule2 = ctrl.Rule(x_ketinggian['rendah'] & x_percepatan['sedang'], x_status['aman'])
        rule3 = ctrl.Rule(x_ketinggian['rendah'] & x_percepatan['cepat'], x_status['siaga'])

        rule4 = ctrl.Rule(x_ketinggian['sedang'] & x_percepatan['lamban'], x_status['siaga'])
        rule5 = ctrl.Rule(x_ketinggian['sedang'] & x_percepatan['sedang'], x_status['siaga'])
        rule6 = ctrl.Rule(x_ketinggian['sedang'] & x_percepatan['cepat'], x_status['bahaya'])

        rule7 = ctrl.Rule(x_ketinggian['tinggi'] & x_percepatan['lamban'], x_status['bahaya'])
        rule8 = ctrl.Rule(x_ketinggian['tinggi'] & x_percepatan['sedang'], x_status['bahaya'])
        rule9 = ctrl.Rule(x_ketinggian['tinggi'] & x_percepatan['cepat'], x_status['bahaya'])

        status_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
        self.status = ctrl.ControlSystemSimulation(status_ctrl)
        
        self.thread = ServerThread()
        self.thread.start()
        self.connect(self.thread, QtCore.SIGNAL("tinggi(float)"), self.tinggi)
        self.connect(self.thread, QtCore.SIGNAL("cepat(float)"), self.cepat)

    def tinggi(self,a):
        self.status.input['ketinggian'] = a
        print("ketinggian in")

    def cepat(self,b):
        self.status.input['percepatan'] = b
        print("percepatan in")
        self.compute()

    def compute(self):
        self.status.compute()
        #self.status.print_state()
        val = max(self.status.output, key=self.status.output.get)
        #print("Nilai Status : {0}".format(self.status.output_status['status']))
        print("Status : {0}".format(val))
        self.emit(QtCore.SIGNAL("fuzzy(QString)"), str(val))

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

        #self.thread = ServerThread()
        #self.thread.start()
        #self.connect(self.thread, QtCore.SIGNAL("tinggi(float)"), self.tinggi)
        #self.connect(self.thread, QtCore.SIGNAL("cepat(float)"), self.cepat)

        self.thread3 = FuzzyThread()
        self.thread3.start()
        self.connect(self.thread3, QtCore.SIGNAL("fuzzy(QString)"), self.doing)

        self.thread = ServerThread()
        self.connect(self.thread, QtCore.SIGNAL("tinggi(float)"), self.tinggi)

    def tinggi(self, a):
        self.ketinggian.display(a)

    def cepat(self, a):
        self.percepatan.display(a)

    def doing(self, a):
        if a == "bahaya" :
            self.dan.setChecked(True)
            self.war.setChecked(False)
            self.ama.setChecked(False)
            x = 1
            self.sendsms(x)
        elif a == "siaga" :
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
