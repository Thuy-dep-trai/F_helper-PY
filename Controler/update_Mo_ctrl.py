from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QMdiSubWindow,QMessageBox
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt
from View import update_Mo
import sys
from Models import db_helper

class update_Mo_ctrl:
    def __init__(self):
        self.view = update_Mo.update_Mo()        
        self.connect_signals()

    def connect_signals(self):
        self.view.txtdata.textChanged.connect(self.txtdata_changed)
        self.view.btnexit.clicked.connect(self.on_btn_exit)
        self.view.btnclear.clicked.connect(self.on_btn_clear)
        self.view.txtmono.returnPressed.connect(self.txtmono_enter)
        self.view.txtun_successfull.textChanged.connect(self.txtdataNG_changed)
        self.view.txtsuccessfull.textChanged.connect(self.txtdataOK_changed)
        self.view.btnselect.clicked.connect(self.btn_select_clicked)
        self.view.btndo_update.clicked.connect(self.on_btn_doupdate)

    def btn_select_clicked(self):
        print("select")
        self.view.table107.setModel(QStandardItemModel())
        if self.view.txtdata.toPlainText():
            txtdata = self.view.txtdata.toPlainText()
            lines = [line.strip() for line in txtdata.splitlines()if  line]
            select_column = next((rb.text() for rb in [self.view.rdosn,self.view.rdomac] if rb.isChecked()), None)
            headers,rows = db_helper.orclquerry_extend("*","sfism4.r107",select_column,lines ,"","")
            self.fill_data_to_table_view( self.view.table107,headers,rows,self.view.lblcount107)
        else:
            print("no data")

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

    def on_btn_clear(self):
        print("clear")
        self.view.txtdata.clear()
        self.view.txtmono.clear()
        self.view.txtsuccessfull.clear()
        self.view.txtun_successfull.clear()
        for tble in [self.view.table105,self.view.table107]:
            tble.setModel(QStandardItemModel())

    def txtmono_enter(self):
        print("mo no enter")
        self.view.table105.setModel(QStandardItemModel())
        mo_number = self.view.txtmono.text().strip().upper()
        if mo_number:
            sql=f"select * from sfism4.r105 where mo_number ='{mo_number}'"
            headers ,rows = db_helper.orclquerry(sql)            
            if len(rows)>0:
                self.fill_data_to_table_view(self.view.table105,headers,rows,self.view.lblcount105)
            else:
                print("no mo_number")
        else:
            print("no mo_number")

    def txtdata_changed(self):
        self.count_line(self.view.txtdata,self.view.lblcountdata,"") 

    def txtdataNG_changed(self):
        self.count_line(self.view.txtun_successfull,self.view.lbl_ng,"UnSuccess ")

    def txtdataOK_changed(self):
        self.count_line(self.view.txtsuccessfull,self.view.lbl_ok,"Success ")         


    def count_line(self,txtdata,lbl,content):
        text = txtdata.toPlainText()
        lines = [line for line in text.splitlines() if line.strip()]
        lbl.setText(f"{content} Count : {len(lines)}")


    def on_btn_doupdate(self):        
        mo_number,model_name,special_route = self.get_mo_route()
        if mo_number and model_name and special_route:
            data107 = self.view.table107.model()
            if data107 is None or data107.rowCount()==0:
                print("no data 107 table")
            else:
                header_map={}
                for col in range(data107.columnCount()):
                    header= data107.headerData(col,Qt.Horizontal)
                    header_map[header]=col
                for row in range(data107.rowCount()):
                    model_107 = data107.index(row,header_map["MODEL_NAME"]).data()
                    serial_number = data107.index(row,header_map["SERIAL_NUMBER"]).data()
                    group_name = data107.index(row,header_map["GROUP_NAME"]).data()
                    if group_name !="SHIPPING" and group_name !="offline":
                        if model_107==model_name:
                            sql=f"update sfism4.r_wip_tracking_t a set a.mo_number='{mo_number}' , a.special_route='{special_route}' where a.serial_number='{serial_number}'"
                            ex_count = db_helper.orcl_execute(sql)
                            if ex_count > 0:
                                self.view.txtsuccessfull.append(serial_number + " go to "+ mo_number)
                            else:
                                self.view.txtun_successfull.append(serial_number)
                        else:
                            self.view.txtun_successfull.append(serial_number)
                    else:
                        self.view.txtun_successfull.append(serial_number)
                    QApplication.processEvents()
        else:
            QMessageBox.information(self.view, "notify", "no data")

    def get_mo_route(self):
        data = self.view.table105.model()
        mo_number=""
        special_route=""
        model=""
        if data is None or data.rowCount() == 0:
            return "", "", ""
        
        for col in range(data.columnCount()):
            header = data.headerData(col, Qt.Horizontal)
            if header == "MO_NUMBER":
                index = data.index(0,col)
                mo_number = data.data(index)
            if header == "ROUTE_CODE":
                index = data.index(0,col)
                special_route = data.data(index)
            if header == "MODEL_NAME":
                index = data.index(0,col)
                model = data.data(index)   
            
        return mo_number,model,special_route        
                        
                                        