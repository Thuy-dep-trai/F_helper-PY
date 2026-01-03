from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QMdiSubWindow
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from View import update_weightGUI
import sys
from Models import db_helper

class update_w_controler:
    def __init__(self):
        self.view = update_weightGUI.Update_weightGui()        
        self.connect_signals()

    def connect_signals(self):
        print("ok")
        self.view.btn_clear.clicked.connect(self.on_btn_Clear_clicked)
        self.view.btn_exit.clicked.connect(self.on_btn_Exit_clicked)
        self.view.btn_save.clicked.connect(self.on_btn_save_clicked)
        self.view.txtmodel.returnPressed.connect(self.press_txtmodel_enter)
        self.view.txtstandw.returnPressed.connect(self.press_txtweight_enter)

    def on_btn_save_clicked(self):
        print("save")
        stand_w = str(self.view.txtstandw.text())
        upper_w = str(self.view.txtupperw.text())
        lower_w = str(self.view.txtlowerw.text())
        model_name = self.view.txtmodel.text()
        if stand_w and upper_w and lower_w and model_name:
            sql=f"update sfis1.c_pn_desc_t a set a.standard_weight={stand_w} , a.upper_weight={upper_w} , a.lower_weight={lower_w} where a.part_no='{model_name}'"
            print(sql)
            row = db_helper.orcl_execute(sql)
            self.view.lblpass.setText(f"successfull : {row}")
            self.view.lblpass.setStyleSheet("color: Green;")
        else:
            self.view.lblpass.setText(f"missing data")
            self.view.lblpass.setStyleSheet("color: red;")


    def on_btn_Clear_clicked(self):
        print("Clear")
        for txt in [self.view.txtlowerw,self.view.txtmodel,self.view.txtstandw,self.view.txtupperw]:
            txt.clear()

    def on_btn_Exit_clicked(self):
        print("exit")
        parent = self.view.parent()
        while parent and not isinstance(parent, QMdiSubWindow):
            parent = parent.parent()

        if parent:
            parent.close()
    
    def press_txtmodel_enter(self):
        print("enter")
        model_name = self.view.txtmodel.text().strip().upper()
        sql = f"select  a.part_no,a.standard_weight,a.upper_weight,a.lower_weight  from sfis1.c_pn_desc_t  a where  a.part_no  = '{model_name}'"
        headers,rows = db_helper.orclquerry(sql)
        if not rows:
            self.view.lblpass.setText("No data")
            self.view.lblpass.setStyleSheet("color: red;")
        else:
            self.view.lblpass.setText("View data")
            self.view.lblpass.setStyleSheet("color: Green;")
            row_dict = dict(zip(headers, rows[0])) 
            self.view.txtmodel.setText(str(row_dict["PART_NO"]))
            self.view.txtstandw.setText(str(row_dict["STANDARD_WEIGHT"]))
            self.view.txtupperw.setText(str(row_dict["UPPER_WEIGHT"]))
            self.view.txtlowerw.setText(str(row_dict["LOWER_WEIGHT"]))
            self.view.txtstandw.setFocus()
            self.view.txtstandw.selectAll()
        
    def press_txtweight_enter(self):
        print("weight enter")
        stand_w = int(float(self.view.txtstandw.text()))
        upper_w=0
        lower_w=0
        diff=0
        if stand_w > 9999:
            diff=100
        elif stand_w <10000:
            diff=10
        upper_w=stand_w+diff
        lower_w= stand_w-diff
        self.view.txtupperw.setText(str(upper_w))
        self.view.txtlowerw.setText(str(lower_w))
            
            