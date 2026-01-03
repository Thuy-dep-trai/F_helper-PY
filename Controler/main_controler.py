from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem,QShortcut,QKeySequence
from Models import db_helper
from utils import excel_helper,CtrC_table
import sys
from PySide6.QtCore import Qt
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex,QSortFilterProxyModel

from View import Main_gui,label_reprintGUI,update_weightGUI
from Controler.label_reprint_ctrl import Label_reprint_controler
from Controler.update_weight_ctr import update_w_controler
from Controler.Coppy_log_ctrl import Coppy_log_ctrl
from Controler.Un_imei_ctrl import Un_imei_ctrl


class Main_controler:
    def __init__(self):
        self.view = Main_gui.Main_gui()        
        self.add_contrl()

    #control
    def add_contrl(self):
        
        self.view.rdo_107.toggled.connect(self.set_rdo)
        self.view.rdo_105.toggled.connect(self.set_rdo)
        self.view.txtdata_edit.textChanged.connect(self.txtdata_count)
        self.view.btnselect.clicked.connect(self.btn_select_clicked)
        self.view.btnexcel.clicked.connect(self.btn_excel_clickes)
        self.view.btnclear.clicked.connect(self.btn_clear_clicked)
        self.view.btnexit.clicked.connect(self.btn_exit_clicked)
        self.view.btn_coppyA.clicked.connect(self.btn_coppyA_clicked)
        self.view.btn_resetA.clicked.connect(self.btn_resetA_clicked)
        self.view.txtdatatab2A.textChanged.connect(self.txtA_count)
        self.view.btnAB.clicked.connect(self.btn_AB_clicked)
        self.view.btn_coppyB.clicked.connect(self.btn_coppyB_clicked)
        self.view.btn_resetB.clicked.connect(self.btn_resetB_clicked)
        self.view.txtdatatab2B.textChanged.connect(self.txtB_count)
        self.view.btn_removedup.clicked.connect(self.btn_removr_dup_clicked)

         # Gắn Ctrl+C cho toàn bộ form
        shortcut = QShortcut(QKeySequence("Ctrl+C"), self.view)
        shortcut.activated.connect(CtrC_table.copy_from_active_table)
        


        


        
    def btn_coppyA_clicked(self):
        print("coppyA")
        txt = self.view.txtdatatab2A.toPlainText()
        QApplication.clipboard().setText(txt)

    def btn_coppyB_clicked(self):
        print("coppyB")
        txt = self.view.txtdatatab2B.toPlainText()
        QApplication.clipboard().setText(txt)

    def btn_resetA_clicked(self):
        print("resetA")
        self.view.txtdatatab2A.clear()

    def btn_resetB_clicked(self):
        print("resetB")
        self.view.txtdatatab2B.clear()

    def btn_AB_clicked(self):
        print("AB")
        text=self.view.txtdatatab2A.toPlainText()
        lines=[line.strip() for line in text.splitlines() if line.strip()]# loại dòng rỗng
        self.view.txtdatatab2B.setText( ",\n".join(f"'{s}'" for s in lines) if lines else"")

    def btn_removr_dup_clicked(self):
        print("remove Dup")
        text=self.view.txtdatatab2A.toPlainText()
        lines=[line.strip() for line in text.splitlines() if line.strip()]# loại dòng rỗng
        # Giữ thứ tự, nhưng loại trùng
        seen = set()
        unique_lines = []
        for line in lines:
            line = line.strip()
            if line and line not in seen:
                unique_lines.append(line)
                seen.add(line)
        
        # Ghi lại nội dung đã loại trùng
        self.view.txtdatatab2B.setText("\n".join(unique_lines))

    def btn_select_clicked(self):
        print("select")
        if self.view.txtdata_edit.toPlainText():
            select_all="*"
            txtdata = self.view.txtdata_edit.toPlainText()
            lines = [line.upper().strip() for line in txtdata.splitlines()if  line]
            select_column = next((rb.text() for rb in self.view.radios if rb.isChecked()), None)
            select_table=next((rb.text() for rb in [self.view.rdo_105,self.view.rdo_107] if rb.isChecked()),None)
            if select_column =="SSID":
                select_table += " a  left join sfis1.u_a56_mac_t b on a.serial_number = b.serial_number " 
                select_column="b.ssid"
                select_all= select_column + ",a.*"
            elif select_column =="DEVKEY":
                select_table += " a  left join sfism4.u_2wire_keys_info_t b on a.serial_number = b.serial_number " 
                select_column="b.devkey"
                select_all= select_column + ",a.*"
            headers,rows = db_helper.orclquerry_extend(select_all,select_table,select_column,lines ,"","")
            self.fill_data_to_table_view(headers,rows)
        else:
            print("no data")

    def btn_excel_clickes(self):
        print("excel")
        excel_helper.export_to_excel_from_tableview(self.view.table_view)
        
    def btn_clear_clicked(self):
        print("clear")
        self.view.txtdata_edit.clear()

        
        model = VAC120TableModel()
        model.reset_data()
        self.view.table_view.setModel(model)
        self.view.lbltablecount.setText("Count: 0")
        




    def btn_exit_clicked(self):
        print("exit")
        sys.exit()

    
    def fill_data_to_table_view(self, headers, rows):
        # Khởi tạo model tùy chỉnh
        model = VAC120TableModel(data=rows, headers=headers)
        
        # Gán model vào bảng
        self.view.table_view.setModel(model)

        # Tùy chỉnh hiển thị
        self.view.table_view.resizeColumnsToContents()
        
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(model)

        self.view.table_view.setModel(proxy_model)
        self.view.table_view.setSortingEnabled(True)

        #self.view.table_view.setEditTriggers(QTableView.NoEditTriggers)  # Ngăn chỉnh sửa

        # Hiển thị số dòng
        row_count = model.rowCount()

        self.view.lbltablecount.setText(f"Count: {row_count}")
        print("view data")
    
    
    def txtdata_count(self):
        self.count_line(self.view.txtdata_edit,self.view.lblcountedittxt,"")
    def txtA_count(self):
        self.count_line(self.view.txtdatatab2A,self.view.lblA,"A")
    def txtB_count(self):
        self.count_line(self.view.txtdatatab2B,self.view.lblB,"B")          
        
    def count_line(self,txtdata,lbl,content):
        text = txtdata.toPlainText()
        lines = [line for line in text.splitlines() if line.strip()]
        lbl.setText(f"{content} Count : {len(lines)}")

    def set_rdo(self):
        if not hasattr(self.view, 'radios'):
            return  # radios chưa khởi tạo, bỏ qua
        if self.view.rdo_105.isChecked():
             hide_list=["Serial_number", "Pallet_no",
                    "Lan_address", "Carton_no",
                     "SSID",       "Po_no",      "DEVKEY" ]
             for rb in self.view.radios:
                 if rb.text() in hide_list:
                     rb.hide()
                 elif rb.text() =="Mo_number":
                     rb.setChecked(True)
                 
                    
        if self.view.rdo_107.isChecked():
             hide_list=["Serial_number", "Pallet_no",
                    "Lan_address", "Carton_no",
                     "SSID",       "Po_no",      "DEVKEY" ]
             for rb in self.view.radios:
                if rb.text() in hide_list:
                     rb.show() 
                


class VAC120TableModel(QAbstractTableModel):
    def __init__(self, data=None, headers=None):
        super().__init__()
        self._data = data if data else []
        self._headers = headers if headers else []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers) if self._headers else (len(self._data[0]) if self._data else 0)

    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            row = index.row()
            col = index.column()
            if row < len(self._data):
                row_data = self._data[row]
                if col < len(row_data):
                    value = row_data[col]
                    return str(value) if value is not None else None  # Không hiển thị nếu là None
        return None


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal and self._headers:
            return self._headers[section]
        if orientation == Qt.Vertical:
            return str(section + 1)
        return None

    def reset_data(self, new_data=None, new_headers=None):
        self.beginResetModel()
        self._data = new_data if new_data else []
        self._headers = new_headers if new_headers else []
        self.endResetModel()

