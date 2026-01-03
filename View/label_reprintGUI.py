from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QLineEdit
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem
import sys
from PySide6.QtCore import Qt

class Label_reprintGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Label_reprint")
        self.resize(1100, 600)  # Rộng 800px, cao 600px

        #add control
        main_layout = QVBoxLayout()# chia hàng dọc

        top_layout = QVBoxLayout()#trên top

        top_layouta=QHBoxLayout()

        top_layouta1=QHBoxLayout()

        self.lbl_mo=QLabel("Mo_number")
        self.txtmo=QLineEdit()
        self.txtmo.setFixedWidth(500)
        top_layouta1.addWidget(self.lbl_mo)
        top_layouta1.addSpacing(10)#khoảng cách
        top_layouta1.addWidget(self.txtmo)       
        top_layouta1.addStretch()  # đẩy phần tử về trái

        top_layouta2=QHBoxLayout()

        top_layouta21=QVBoxLayout()
        self.btnreprint=QPushButton("Reprint")
        self.btnclear=QPushButton("Clear")
        top_layouta21.addWidget(self.btnreprint)
        top_layouta21.addWidget(self.btnclear)

        top_layouta22=QVBoxLayout()
        self.btnexit=QPushButton("Exit")
        top_layouta22.addWidget(self.btnexit)

        top_layouta2.addLayout(top_layouta21)
        top_layouta2.addLayout(top_layouta22)
        top_layouta2.addStretch()

        top_layouta.addLayout(top_layouta1,1)
        top_layouta.addLayout(top_layouta2,1)
        

        top_layout.addLayout(top_layouta)

        #bên dưới là bảng
        bot_layout=QVBoxLayout()
        
        self.table_view1 = QTableView()

        self.table_view2 = QTableView()
        # CSS cho bảng (bao gồm cả viền cột)
        
        for tb in [self.table_view1,self.table_view2]:
            tb.setStyleSheet("""
        QTableView {
            background-color: #f0f0f0;
            selection-background-color: #3399FF;  /* Màu nền khi chọn */
            selection-color: red;              /* Màu chữ khi chọn */
            border: 1px solid #aaa;
            gridline-color: #aaa;
            font-size: 13px;
        }

        QTableView::item {
            background-color: white;
        }

        QHeaderView::section {
            background-color: #e0e0e0;
            padding: 4px;
            border: 1px solid #aaa;
            font-weight: bold;
        }

        QTableCornerButton::section {
            background-color: #e0e0e0;
            border: 1px solid #aaa;
        }
    """)
        bot_layout.addWidget(self.table_view1)
        self.table_view1.setFixedHeight(150)
        self.lbltablecount = QLabel("Rows count:")  
        bot_layout.addWidget(self.lbltablecount)
        bot_layout.addWidget(self.table_view2)
        self.lbl_result= QLabel("Result")
        bot_layout.addWidget(self.lbl_result)
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bot_layout)

        # tô màu cho btn
        for btn in [self.btnclear,self.btnexit,self.btnreprint]:
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
            btn.setFixedSize(100,40)
        self.setLayout(main_layout)

