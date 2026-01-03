from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QLineEdit,QFormLayout
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem,QIntValidator
import sys
from PySide6.QtCore import Qt

class Coppy_logGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Coppy Log")
        self.resize(1100, 600)  # Rộng 800px, cao 600px  
        self.adjustSize()  # ← Đảm bảo layout được tính toán đúng      

        # tạo các contrl
        #form của cả main
        Qform = QFormLayout()
        #main layout cho tất cả 
        main_layout = QHBoxLayout()#hàng ngang
        #layout chia đôi
        #layout bên trái
        left_layout=QVBoxLayout()
    
        #layout bên trái chia đôi : bên trên
        left_layout_v_1a = QVBoxLayout()

        left_layout_v_1a1 = QHBoxLayout() # layout chia 3 hàng ngang

        left_layout_v_1a1_1 = QVBoxLayout() # hàng 1 

        self.lblcount_data=QLabel("SN Count: ")
        self.txtdata=QTextEdit()

        left_layout_v_1a1_1.addWidget(self.lblcount_data)
        left_layout_v_1a1_1.addWidget(self.txtdata)

        left_layout_v_1a1_2 = QVBoxLayout() # hàng 2

        self.group_db = QGroupBox("Database")
        self.group_db.setFixedSize(100,80)
        group_db_layout=QVBoxLayout()
        self.rdo_avc = QRadioButton("avc")   
        self.rdo_avc.setChecked(True)     
        self.rdo_cnc = QRadioButton("cnc")
        group_db_layout.addWidget(self.rdo_avc)
        group_db_layout.addWidget(self.rdo_cnc)
        self.group_db.setLayout(group_db_layout)

        self.group_type = QGroupBox("Type coppy")
        self.group_type.setFixedSize(100,80)
        group_type_layout=QVBoxLayout()
        self.rdo_Log = QRadioButton("Log file")   
        self.rdo_Log.setChecked(True)     
        self.rdo_cal = QRadioButton("Cal file")
        group_type_layout.addWidget(self.rdo_Log)
        group_type_layout.addWidget(self.rdo_cal)
        self.group_type.setLayout(group_type_layout)

        
        self.btn_go= QPushButton("Go")
        self.btnreset= QPushButton("Reset")
        self.btnrexit= QPushButton("Exit")
        
        left_layout_v_1a1_2.addWidget(self.group_db)
        left_layout_v_1a1_2.addWidget(self.group_type)
        left_layout_v_1a1_2.addSpacing(60)
        left_layout_v_1a1_2.addWidget(self.btn_go)
        left_layout_v_1a1_2.addWidget(self.btnreset)
        left_layout_v_1a1_2.addWidget(self.btnrexit)
        # Thêm dòng này để đẩy toàn bộ các widget lên trên
        left_layout_v_1a1_2.addStretch()
       

        left_layout_v_1a1_3 = QVBoxLayout() # hàng 3

        self.lblcount_result=QLabel("Path result Count: ")
        self.txtresult=QTextEdit()

        left_layout_v_1a1_3.addWidget(self.lblcount_result)
        left_layout_v_1a1_3.addWidget(self.txtresult)


        #add vào lay out 
        left_layout_v_1a1.addLayout(left_layout_v_1a1_1,4)
        left_layout_v_1a1.addLayout(left_layout_v_1a1_2,1)
        left_layout_v_1a1.addLayout(left_layout_v_1a1_3,8)

        left_layout_v_1a.addLayout(left_layout_v_1a1)

        #layout bên trái ở dưới
        left_layout_v_1b = QVBoxLayout()

        left_layout_v_1b_1=QHBoxLayout()
        #self.lblpathTo=QLabel("Coppy to")
        self.btn_coppyto=QPushButton("Coppy to")
        self.txtcoppyto=QLineEdit()
        #left_layout_v_1b_1.addWidget(self.lblpathTo)
        left_layout_v_1b_1.addWidget(self.btn_coppyto)
        left_layout_v_1b_1.addWidget(self.txtcoppyto)

        

        left_layout_v_1b_2=QHBoxLayout()
        self.lblgroup=QLabel("Group    ")
        self.txtgroup=QLineEdit()
        left_layout_v_1b_2.addWidget(self.lblgroup)
        left_layout_v_1b_2.addWidget(self.txtgroup)

        


        left_layout_v_1b_3=QHBoxLayout()
        self.lblpathfrom=QLabel("Path       ")
        self.txtpathfrom=QTextEdit()
        left_layout_v_1b_3.addWidget(self.lblpathfrom)
        left_layout_v_1b_3.addWidget(self.txtpathfrom)

        left_layout_v_1b.addLayout(left_layout_v_1b_1,1)
        left_layout_v_1b.addLayout(left_layout_v_1b_2,1)
        left_layout_v_1b.addLayout(left_layout_v_1b_3,3)

        left_layout.addLayout(left_layout_v_1a,3)
        left_layout.addLayout(left_layout_v_1b,1)
        
       

        #layout cho bên phải
        right_layout=QVBoxLayout()

        self.lblcountNG=QLabel("NG Count: ")
        self.txtNG = QTextEdit()

        right_layout.addWidget(self.lblcountNG)
        right_layout.addWidget(self.txtNG)
        # tô màu btn 
        for btn in [ self.btn_go,self.btnreset,self.btnrexit,self.btn_coppyto]:
            btn.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;      /* Xanh dương nhạt */
                color: black;                   /* Màu chữ */
                border: 1px solid #7fb1cc;      /* Viền xanh dương hơi đậm */
                border-radius: 12px;             /* Bo góc */
                padding: 6px 12px;              /* Đệm trong nút */
                font-size: 13px;
            }

            QPushButton:hover {
                background-color: #bfe3f4;      /* Hiệu ứng khi rê chuột */
            }

            QPushButton:pressed {
                background-color: #91c9e8;      /* Hiệu ứng khi nhấn nút */
            }
        """)
        for txt in [self.txtdata,self.txtNG,self.txtpathfrom,self.txtresult]:
            txt.setAcceptRichText(False)

        # mainlayout
        main_layout.addLayout(left_layout,4)
        main_layout.addLayout(right_layout,1)

        self.setLayout(main_layout)
