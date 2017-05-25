from PyQt4 import QtSql, QtGui

def createDB():
   db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
   db.setDatabaseName('data.db')
	
   if not db.open():
      QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
         QtGui.qApp.tr("Unable to establish a database connection.\n"
            "This example needs SQLite support. Please read "
            "the Qt SQL driver documentation for information "
            "how to build it.\n\n" "Click Cancel to exit."),
         QtGui.QMessageBox.Cancel)
			
      return False
		
   query = QtSql.QSqlQuery(db)
	
   query.exec_("create table data_diri(id int primary key, "
      "nama varchar(20), nohp varchar(20))")
		
   query.exec_("insert into data_diri values(1, 'Adryan Chiko', '085706000014')")
   return True
   db.close()
	
if __name__ == '__main__':
   import sys
	
   app = QtGui.QApplication(sys.argv)
   createDB()