from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QLineEdit,QFormLayout
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem,QIntValidator
import sys
from PySide6.QtCore import Qt

class Unimei_GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Un_Imei")
        self.resize(1200, 700)  # Rộng 800px, cao 600px

        main_layout = QHBoxLayout()# layout chính ngang

        main_layout_left = QVBoxLayout()# layout ngang bên trái

        main_layout_left1 = QHBoxLayout()
        self.lblrequest = QLabel("request by")
        self.txtrequestby = QLineEdit()
        main_layout_left1.addWidget(self.lblrequest)
        main_layout_left1.addWidget(self.txtrequestby)
        main_layout_left.addLayout(main_layout_left1)

        group_type=QGroupBox("Type")
        group_type.setFixedWidth(350)
        group_layout = QHBoxLayout()# layout chính trong group là ngang
        self.rdosn = QRadioButton("Serial_number")
        self.rdosn.setChecked(True)
        self.rdomac = QRadioButton("Lan_address")
        self.rdoimei = QRadioButton("Imei")
        group_layout.addWidget(self.rdosn )
        group_layout.addWidget(self.rdomac )
        group_layout.addWidget(self.rdoimei )
        group_type.setLayout(group_layout)
        main_layout_left.addWidget(group_type)

        main_layout_left2= QHBoxLayout()# layout bên dưới bên trái

        main_layout_left2_1 = QVBoxLayout()
        self.lblcountdata = QLabel("Data")
        self.txtdata = QTextEdit()
        self.txtdata.setAcceptRichText(False)
        self.txtdata.setFixedWidth(200)
        self.txtdata.setStyleSheet("""
            QTextEdit {
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 6px;
                background-color: #dcdcdc;
                font-size: 14px;
                font-family: Consolas;
            }
        """)
        main_layout_left2_1.addWidget(self.lblcountdata)
        main_layout_left2_1.addWidget(self.txtdata)

        main_layout_left2_2 = QVBoxLayout()
        self.btnselect = QPushButton("Select")
        self.btnunimei = QPushButton("Un_imei")
        self.btnclear = QPushButton("Clear")
        self.btnexit= QPushButton("Exit")
        for btn in [ self.btnselect,self.btnunimei,self.btnclear,self.btnexit]:
            btn.setFixedSize(100,40)
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
        main_layout_left2_2.addSpacing(100)
        main_layout_left2_2.addWidget(self.btnselect)
        main_layout_left2_2.addSpacing(20)
        main_layout_left2_2.addWidget(self.btnunimei)
        main_layout_left2_2.addSpacing(20)
        main_layout_left2_2.addWidget(self.btnclear)
        main_layout_left2_2.addSpacing(10)
        main_layout_left2_2.addWidget(self.btnexit)
        main_layout_left2_2.addStretch()

        main_layout_left2.addLayout(main_layout_left2_1)
        main_layout_left2.addLayout(main_layout_left2_2)

        main_layout_left.addLayout(main_layout_left2)

        main_layout_right = QVBoxLayout()# layout ngang bên phải
        self.lblcountorcl= QLabel("Count")
        self.tablevieworcl=QTableView()
        self.lblcountsql = QLabel("Count")
        self.tableviewsql = QTableView()
        self.tableviewsql.setEditTriggers(QTableView.NoEditTriggers)  # ← Cấm chỉnh sửa
        main_layout_right.addWidget(self.lblcountorcl)
        main_layout_right.addWidget(self.tablevieworcl)
        main_layout_right.addWidget(self.lblcountsql)
        main_layout_right.addWidget(self.tableviewsql)
        for tableview in [self.tablevieworcl,self.tableviewsql]:
            tableview.setStyleSheet("""
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

        main_layout.addLayout(main_layout_left,1)
        main_layout.addLayout(main_layout_right,3)

        self.setLayout(main_layout)
        
        


        # tạo các contrl
       

       
        
       
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Unimei_GUI()
    form.show()
    sys.exit(app.exec())