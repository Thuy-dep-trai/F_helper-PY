from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QMdiSubWindow
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from View import label_reprintGUI
import sys
from Models import db_helper

class Label_reprint_controler:
    def __init__(self):
        self.view = label_reprintGUI.Label_reprintGUI()        
        self.connect_signals()

    def connect_signals(self):
        self.view.btnreprint.clicked.connect(self.on_btnreprint_clicked)
        self.view.btnclear.clicked.connect(self.on_btnClear_clicked)
        self.view.btnexit.clicked.connect(self.on_btnexit_clicked)
        self.view.txtmo.returnPressed.connect(self.on_txtmo_enter)


    def on_btnreprint_clicked(self):
        print("reprint")
        mo_number = self.view.txtmo.text().strip().upper()
        if mo_number:
            sql=f"update sfism4.r107 a set a.section_flag='0' where a.mo_number='{mo_number}' and a.section_flag='1' and a.group_name='0' and substr(a.mo_number,0,1) in ('N','S')"
            successfull = db_helper.orcl_execute(sql)
            print(successfull)
            self.view.lbl_result.setText(f"succesfull count : {successfull}")
        else:
            print("no mo")
    
    def on_btnClear_clicked(self):
        print("Clear")
        self.view.txtmo.clear()
        self.view.table_view1.setModel(QStandardItemModel())
        self.view.table_view2.setModel(QStandardItemModel())

    def on_btnexit_clicked(self):
        print("exit")
        parent = self.view.parent()
        while parent and not isinstance(parent, QMdiSubWindow):
            parent = parent.parent()

        if parent:
            parent.close()
            

    def on_txtmo_enter(self):
        print("enter txt")
        mo_number = self.view.txtmo.text().strip().upper()
        sql=f"select * from sfism4.r107 where mo_number = '{mo_number}'"
        headers , rows = db_helper.orclquerry(sql)
        self.fill_data_to_table_view(self.view.table_view2,headers,rows,self.view.lbltablecount)

        sql2 = f"""
                SELECT a.mo_number, a.model_name, a.section_flag, a.group_name, a.next_station, COUNT(*) 
                FROM sfism4.r107 a 
                WHERE a.mo_number = '{mo_number}' 
                GROUP BY a.mo_number, a.model_name, a.section_flag, a.group_name, a.next_station
                """
        headers2,rows2 = db_helper.orclquerry(sql2)
        self.fill_data_to_table_view(self.view.table_view1,headers2,rows2)

    def fill_data_to_table_view(self,tableview,headers,rows,lblcount=""):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(headers)        
        for row in rows:
            items = []
            for cell in row:
                item = QStandardItem(str(cell) if cell is not None else "")
                #item.setEditable(False)  # Không cho chỉnh sửa cell
                items.append(item)
            model.appendRow(items)

        tableview.setModel(model)
         # Quan trọng: ngăn chế độ chỉnh sửa khi click vào cell
        #self.table_view.setEditTriggers(QTableView.NoEditTriggers)
        tableview.resizeColumnsToContents()
        tableview.setSortingEnabled(True)
        row_count = tableview.model().rowCount()
        if  lblcount:
            lblcount.setText(f"Count: {row_count}")
        

    