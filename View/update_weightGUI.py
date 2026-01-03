from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QLineEdit,QFormLayout
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem,QIntValidator
import sys
from PySide6.QtCore import Qt

class Update_weightGui(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update weight")
        self.setFixedSize(500, 250)  # Rộng 800px, cao 600px
        #self.setStyleSheet("background-color: #c0c0c0;")  # xám vừa
         # Tạo vùng MDI


        # tạo các contrl
        main_layout = QHBoxLayout()
        main_layout_left = QVBoxLayout()
        Qform = QFormLayout()
        self.lblmodel=QLabel("Model_name")
        self.lblstandw= QLabel("StandWeight")
        self.lblupperw = QLabel("UpperWeight")
        self.lbllowerw = QLabel("LowerWeight")
        

        right_layout= QVBoxLayout()
        self.txtmodel= QLineEdit()
        self.txtstandw= QLineEdit()
        self.txtupperw= QLineEdit()
        self.txtlowerw= QLineEdit()
        
        # for txt in [self.txtlowerw,self.txtstandw,self.txtupperw]:
        #     txt.setValidator(QIntValidator(0, 100000))

        layout1 = QHBoxLayout()
        layout1.addWidget(self.lblmodel)
        layout1.addWidget(self.txtmodel)
        layout1.addSpacing(50)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.lblstandw)
        layout2.addWidget(self.txtstandw)
        layout2.addSpacing(50)

        layout3 = QHBoxLayout()
        layout3.addWidget(self.lblupperw)
        layout3.addWidget(self.txtupperw)
        layout3.addSpacing(50)

        layout4 = QHBoxLayout()
        layout4.addWidget(self.lbllowerw)
        layout4.addWidget(self.txtlowerw)
        layout4.addSpacing(50)

        

        main_layout_left.addLayout(layout1)
        main_layout_left.addSpacing(20)
        main_layout_left.addLayout(layout2)
        main_layout_left.addSpacing(20)
        main_layout_left.addLayout(layout3)
        main_layout_left.addSpacing(20)
        main_layout_left.addLayout(layout4)
        main_layout_left.addSpacing(20)

        main_layout_right=QVBoxLayout()

        self.btn_save=QPushButton("Save")
        self.btn_clear=QPushButton("Clear")
        self.btn_exit=QPushButton("Exit")
        main_layout_right.addWidget(self.btn_save)
        main_layout_right.addSpacing(20)
        main_layout_right.addWidget(self.btn_clear)
        main_layout_right.addSpacing(20)
        main_layout_right.addWidget(self.btn_exit)


        # tô màu btn 
        for btn in [ self.btn_clear,self.btn_exit,self.btn_save]:
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

        main_layout.addLayout(main_layout_left)
        main_layout.addLayout(main_layout_right)
        self.lblpass=QLabel("Result")

        Qform.addRow(main_layout)
        Qform.addRow(self.lblpass)
        
        self.setLayout(Qform)
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Update_weightGui()
    form.show()
    sys.exit(app.exec())