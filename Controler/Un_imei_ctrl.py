from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QFileDialog,
    QMessageBox,QMdiSubWindow
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QThread, Signal, QObject
from View import un_imei
import sys
from Models import db_helper
import os
import glob
from utils import coppy_cal,excel_helper
from datetime import datetime


class Un_imei_ctrl:
    def __init__(self):
        self.view = un_imei.Unimei_GUI()        
        self.connect_signals()
        self.table = ""
        self.column= ""        
        


    def connect_signals(self):
        print("ok")
        self.view.txtdata.textChanged.connect(self.txtdata_changed)
        self.view.btnclear.clicked.connect(self.on_btn_clear)
        self.view.btnexit.clicked.connect(self.on_btn_exit)
        self.view.btnselect.clicked.connect(self.on_btn_select)
        self.view.btnunimei.clicked.connect(self.on_btn_unimei)
    
    def txtdata_changed(self):
        self.count_line(self.view.txtdata,self.view.lblcountdata,"")          


    def count_line(self,txtdata,lbl,content):
        text = txtdata.toPlainText()
        lines = [line for line in text.splitlines() if line.strip()]
        lbl.setText(f"{content} Count : {len(lines)}")
        
    def on_btn_select(self):
        print("Select")
        if self.view.txtdata.toPlainText():
            for tble in [self.view.tablevieworcl,self.view.tableviewsql]:
                tble.setModel(QStandardItemModel())
            txtdata = self.view.txtdata.toPlainText()
            lines =[line.strip().upper() for line in txtdata.splitlines() if line.strip()]
            if not self.view.rdoimei.isChecked():            
                column=""
                for rdo in [self.view.rdomac,self.view.rdosn]:
                    if rdo.isChecked():
                        column= rdo.text()
                headers,rows = db_helper.orclquerry_extend("*","sfism4.r107",column,lines)
                self.fill_data_to_table_view(self.view.tablevieworcl,headers,rows,self.view.lblcountorcl)
            imei_headers,imei_rows=self.get_imei(lines)
            self.fill_data_to_table_view(self.view.tableviewsql,imei_headers,imei_rows,self.view.lblcountsql)
        else:
            print("no data input")

        

    def on_btn_unimei(self):
        print("UnImei")
        #backup
        data_sql = self.view.tableviewsql.model()
        if data_sql is not None and data_sql.rowCount() > 0:
            print("bacup")
            path = r"D:\data_backup_imei"
            os.makedirs(path, exist_ok=True)
            if os.path.isdir(path):
                path=os.path.join(path,datetime.now().strftime("%Y%m%d.%H%M%S")+".xlsx")
                if excel_helper.export_to_excel_from_tableview(self.view.tableviewsql,path):
                    data_column = -1
                    for col in range(data_sql.columnCount()):
                        header = data_sql.headerData(col, Qt.Horizontal)
                        if header == self.column:
                            data_column = col
                            break
                    if data_column!= -1:
                        row_ok=0
                        for row in range(data_sql.rowCount()):
                            index = data_sql.index(row,data_column)
                            value = data_sql.data(index)
                            sql_del=""
                            if self.table=="VR..VR_46BE_IMEI_IN":
                                sql_del = f"update {self.table} set MAIN_BOARD_SN='' where {self.column}='{value}'"    
                            else:
                                sql_del = f"delete from {self.table} where {self.column}='{value}'"                                                        
                            print(sql_del)
                            row_ok += db_helper.sql_execute(sql_del)
                        QMessageBox.information(self.view, "notify", f"delete {row_ok} row")
                    
                else:
                    QMessageBox.information(self.view, "notify", "backup fail")
            else:
                QMessageBox.information(self.view, "notify", "backup fail")
        else:
            QMessageBox.information(self.view, "notify", "no data")


    def on_btn_clear(self):
        print("clear")
        self.view.txtdata.clear()
        for tble in [self.view.tablevieworcl,self.view.tableviewsql]:
            tble.setModel(QStandardItemModel())

    def on_btn_exit(self):
        print("exit")
        parent = self.view.parent()
        while parent and not isinstance(parent, QMdiSubWindow):
            parent = parent.parent()

        if parent:
            parent.close()


    def fill_data_to_table_view(self, table_view,headers,rows,lbltablecount):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)        
        for row in rows:
            items = []
            for cell in row:
                item = QStandardItem(str(cell) if cell is not None else "")
                #item.setEditable(False)  # Không cho chỉnh sửa cell
                items.append(item)
            model.appendRow(items)

        table_view.setModel(model)
         # Quan trọng: ngăn chế độ chỉnh sửa khi click vào cell
        #self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        table_view.resizeColumnsToContents()
        table_view.setSortingEnabled(True)
        row_count = table_view.model().rowCount()
        lbltablecount.setText(f"Count: {row_count}")
        print("view data")



    def get_imei(self,lines):
        data = ",".join(f"'{line}'" for line in lines)
        sql_gettable="select * from tbilly.avc_rules_table_imei"
        headers,rows=db_helper.orclquerry(sql_gettable)  
        for row in rows:
            rowdict = dict(zip(headers,row))
            TABLE_NAME = rowdict["TABLE_NAME"]                        
            print(TABLE_NAME)
            if TABLE_NAME == "TG..TG_IMEI":
                print("no table")
            SN_COLUMN= rowdict["SN_COLUMN"]
            MAC_COLUMN= rowdict["MAC_COLUMN"]
            IMEI_COLUMN= rowdict["IMEI_COLUMN"]            
            sql_getimei=""
            if self.view.rdoimei.isChecked():
                if TABLE_NAME=="MG.dbo.MG_IMEI":
                    data=",".join(f"'{line[0:len(line)-1]}'" for line in lines)
                sql_getimei=f"select * from {TABLE_NAME} where {IMEI_COLUMN} in ({data})"
                self.table= TABLE_NAME
                self.column=IMEI_COLUMN
            elif SN_COLUMN and self.view.rdosn.isChecked():
                sql_getimei=f"select * from {TABLE_NAME} where {SN_COLUMN} in ({data})"
                self.table= TABLE_NAME
                self.column=SN_COLUMN
            elif MAC_COLUMN and self.view.rdomac.isChecked():
                sql_getimei=f"select * from {TABLE_NAME} where {MAC_COLUMN} in ({data})"
                self.table= TABLE_NAME
                self.column=MAC_COLUMN
            else :
                print(f"{TABLE_NAME} not match")
                continue
                
            print(sql_getimei)
            headers_imei,rows_imei=db_helper.sqlquerry(sql_getimei)
            if rows_imei:
                return headers_imei,rows_imei
        return [],[]


    
        