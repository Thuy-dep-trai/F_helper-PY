from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QFileDialog,QMdiSubWindow
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt,QThread, Signal, QObject
from View import Coppy_logGUI
import sys
from Models import db_helper
import os
import glob
from utils import coppy_cal
from Worker_UI import Coppy

class Coppy_log_ctrl:
    def __init__(self):
        self.view = Coppy_logGUI.Coppy_logGUI()        
        self.connect_signals()
        self.avc_db = True
        self.coppylog = True
        self.set_rdo()


    def connect_signals(self):
        print("ok")
        self.view.btn_go.clicked.connect(self.on_btn_go_clicked)
        self.view.btnreset.clicked.connect(self.on_btn_clear_clicked)
        self.view.btnrexit.clicked.connect(self.on_btn_exit_clicked)
        self.view.txtdata.textChanged.connect(self.txtdata_changed)
        self.view.txtresult.textChanged.connect(self.txtrss_changed)
        self.view.txtNG.textChanged.connect(self.txtNG_changed)
        self.view.rdo_avc.clicked.connect(self.rdo_avc_clicked)
        self.view.rdo_cnc.clicked.connect(self.rdo_cnc_clicked)
        self.view.rdo_Log.clicked.connect(self.rdo_coppylog_clicked)
        self.view.rdo_cal.clicked.connect(self.rdo_coppycal_clicked)
        self.view.btn_coppyto.clicked.connect(self.on_btn_coppyTo)
    
    

    def on_btn_go_clicked(self):
        print("go")
        print(self.coppylog)
        if self.coppylog :
            self.coppy_log_threaded()
        else:
            self.coppy_cal_threaded()
        
        
    def on_btn_clear_clicked(self):
        for txt in [self.view.txtdata,self.view.txtNG,self.view.txtresult]:
            txt.clear()
        print("clear")
    def on_btn_exit_clicked(self):
        print("exit")
        parent = self.view.parent()
        while parent and not isinstance(parent, QMdiSubWindow):
            parent = parent.parent()

        if parent:
            parent.close()
    
    def txtdata_changed(self):
        self.count_line(self.view.txtdata,self.view.lblcount_data,"")          

    def txtrss_changed(self):
        self.count_line(self.view.txtresult,self.view.lblcount_result,"")  

    def txtNG_changed(self):
        self.count_line(self.view.txtNG,self.view.lblcountNG,"")  

    def rdo_avc_clicked(self):
        print("")
        self.set_rdo()
    def rdo_cnc_clicked(self):
        print("")
        self.set_rdo()

    def rdo_coppylog_clicked(self):
        print("")
        self.set_rdo()

    def rdo_coppycal_clicked(self):
        print("")
        self.set_rdo()

    def count_line(self,txtdata,lbl,content):
        text = txtdata.toPlainText()
        lines = [line for line in text.splitlines() if line.strip()]
        lbl.setText(f"{content} Count : {len(lines)}")

    def set_rdo(self):      
        if self.view.rdo_avc.isChecked():
            self.avc_db= True
            self.view.txtpathfrom.setPlainText(r"\\10.120.15.43\avc_test_log_file")
        if self.view.rdo_cnc.isChecked():
            self.avc_db= False  
        if self.view.rdo_Log.isChecked():   
            self.view.txtgroup.show()
            self.view.lblgroup.show()         
            self.coppylog = True
            self.view.group_db.show()
            if self.avc_db:
                self.view.txtpathfrom.setPlainText(r"\\10.120.15.43\avc_test_log_file")
            else:
                paths = [
                    r"\\10.130.15.43\avc_test_log_file_2022h1",
                    r"\\10.130.15.43\avc_test_log_file_2023h1",
                    r"\\10.130.15.43\avc_test_log_file_2024h1",
                    r"\\10.130.15.43\test_log_file_2022h1",
                    r"\\10.130.15.43\test_log_file_2021h1",
                    r"\\10.130.15.43\cnc_backup\CNC_TEST_LOG_FILE_2",
                    r"\\10.130.15.43\cnc_backup\CNC_TEST_LOG_FILE_2021H1",
                    r"\\10.130.15.43\cnc_backup\CNC_TEST_LOG_FILE_2022H1",
                    r"\\10.130.15.43\cnc_backup\CNC_TEST_LOG_FILE_2023H1"   
                    ]
                self.view.txtpathfrom.setPlainText("\n".join(paths))
        if self.view.rdo_cal.isChecked():
            self.view.txtgroup.hide()
            self.view.lblgroup.hide()
            self.coppylog = False
            self.view.group_db.hide()
            self.view.txtpathfrom.setPlainText(r"\\10.120.32.250\avc_mfg\Magee_Hsia\HDCP_CAL")

    

    def on_btn_coppyTo(self):
        coppy_to_path = QFileDialog.getExistingDirectory(None, "Select directory", "")
        if coppy_to_path:
            print("Coppy To:", coppy_to_path)
            self.view.txtcoppyto.setText(coppy_to_path)




    def coppy_log_threaded(self):
        self.thread = QThread()
        self.worker = Coppy.CoppyLogWorker(self.view, self.avc_db)
        self.worker.moveToThread(self.thread)

        # Kết nối tín hiệu để cập nhật UI
        self.worker.progress.connect(self.view.btn_go.setText)
        self.worker.result_file.connect(self.view.txtresult.append)
        self.worker.result_ng.connect(self.view.txtNG.append)

        self.thread.started.connect(self.worker.run_coppy_log)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def coppy_cal_threaded(self):
        self.thread = QThread()
        self.worker = Coppy.CoppyLogWorker(self.view, self.avc_db)
        self.worker.moveToThread(self.thread)

        # Kết nối tín hiệu để cập nhật UI
        self.worker.progress.connect(self.view.btn_go.setText)
        self.worker.result_file.connect(self.view.txtresult.append)
        self.worker.result_ng.connect(self.view.txtNG.append)

        self.thread.started.connect(self.worker.run_coppy_cal)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()




    
        