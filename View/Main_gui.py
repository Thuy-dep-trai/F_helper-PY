from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox,
    QRadioButton, QButtonGroup, QGroupBox, QLabel, QTextEdit, QPushButton,
    QTableView, QTabWidget, QMainWindow,QMenuBar,QTableView,QMdiArea,QMenu
)
import os
from PySide6.QtGui import QAction,QStandardItemModel, QStandardItem,QIcon
import sys
from PySide6.QtCore import Qt

class Main_gui(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Fhelper")
        self.resize(1300, 700)  # Rộng 800px, cao 600px
        #self.setStyleSheet("background-color: #c0c0c0;")  # xám vừa
         # Tạo vùng MDI
        
        
        #add control
        #add menubar 
        #layout chính chia làm 2 phần 
        tabhome_layout=QVBoxLayout()

        

        #add phần dưới menubar
        top_panel= QHBoxLayout()
        
        #panel 1 gồm 1 cột chứa group và txtdata
        panel1 =QVBoxLayout()

        #panel chọn bảng 
        panel_table_layout=QVBoxLayout()
        group_t=QGroupBox("")
        group_t.setFixedWidth(350)
        group_t_layout=QHBoxLayout()
        self.rdo_107 = QRadioButton("sfism4.r_wip_tracking_t")        
        self.rdo_105 = QRadioButton("sfism4.r_mo_base_t")
        for rdo in [self.rdo_107,self.rdo_105]:
            rdo.setStyleSheet("""
                QRadioButton {
                    color: #2980b9;
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                    
                }
            """)
        group_t_layout.addWidget(self.rdo_107)
        group_t_layout.addWidget(self.rdo_105)
        self.rdo_107.setChecked(True)

        group_t.setLayout(group_t_layout)

        panel_table_layout.addWidget(group_t)
        panel1.addLayout(panel_table_layout)
        # end tạo group box chọn bảng

        # panel này cho group chọn cột
        panel1_1=QVBoxLayout()
        
        group_type=QGroupBox("Type")
        group_type.setFixedWidth(350)
        #group
        group_layout=QVBoxLayout()# layout chính là dọc
        labels = ["Serial_number", "Mo_number", "Pallet_no",
                   "Lan_address", "Model_name", "Carton_no",
                    "SSID",       "Po_no",      "DEVKEY" ]
        #thêm 4 dòng , mỗi dòng 3 nút
        self.radios=[]
        for i in range(0,10,3):
            row_gr_layout=QHBoxLayout()
            for label in labels[i:i+3]:
                rb=QRadioButton(label)
                self.radios.append(rb)
                row_gr_layout.addWidget(rb)
            group_layout.addLayout(row_gr_layout)            
        self.radios[0].setChecked(True)  # chọn mặc định
        for rb in self.radios:
            rb.setStyleSheet("""
                QRadioButton {
                    color: #2980b9;
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                    
                }
            """)
        group_type.setLayout(group_layout)
        

        
       
        # add vào panel1
        panel1_1.addWidget(group_type)
        #panel1.addWidget(self.txtdata_edit)
        

        # panel này dưới group chọn cột 
        panel1_2 = QHBoxLayout()
        #button ở giữa
         #txtdata
        under_grlayout=QVBoxLayout()

        under_grlayout1=QVBoxLayout()
        self.lblcountedittxt = QLabel("Count")        
        under_grlayout1.addWidget(self.lblcountedittxt)

        self.txtdata_edit=QTextEdit()
        self.txtdata_edit.setFixedWidth(200)
        
        self.txtdata_edit.setAcceptRichText(False)

        
        under_grlayout1.addWidget(self.txtdata_edit)
        under_grlayout.addLayout(under_grlayout1)
        btn_layout=QVBoxLayout()

        self.btnselect=QPushButton("Select")
        self.btnselect.setFixedSize(100,40)
       
        



        self.btnexcel=QPushButton("Export \nto excel")
        self.btnexcel.setFixedSize(100,50)
        


        self.btnclear=QPushButton("Clear")
        self.btnclear.setFixedSize(100,40)
        


        self.btnexit=QPushButton("Exit")
        self.btnexit.setFixedSize(100,40)
        

        

        btn_layout.addSpacing(50)
        btn_layout.addWidget(self.btnselect)
        btn_layout.addWidget(self.btnclear)
        btn_layout.addWidget(self.btnexcel)
        btn_layout.addWidget(self.btnexit)
        btn_layout.addStretch()
        btn_layout.setSpacing(30)  #

        #View lớn
        table_view_layout=QVBoxLayout()      
        self.lbltablecount = QLabel("Rows count:")  
        table_view_layout.addWidget(self.lbltablecount)
        self.table_view = QTableView()
        # CSS cho bảng (bao gồm cả viền cột)
        

        self.table_view.setStyleSheet("""
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


        table_view_layout.addWidget(self.table_view)
        

       

        panel1_2.addLayout(under_grlayout)
        panel1_2.addLayout(btn_layout)

        panel1.addLayout(panel1_1)
        panel1.addLayout(panel1_2)
        top_panel.addLayout(panel1)# add vào left     
        #top_panel.addLayout(under_grlayout,1)# add vào left 
        top_panel.addLayout(table_view_layout)# add vào right
         # Thêm vào layout chính
        #tabhome_layout.addLayout(menuBar_layout)     # phần control: chiếm 1 phần
        #tabhome_layout.addLayout(top_panel)
        #self.setLayout(main_layout) 

                # Tạo Tab chính
        self.tab = QTabWidget()

        # Tab 1: giao diện bạn đã thiết kế ở trên
        tabhome = QWidget()
        tabhome_layout = QVBoxLayout()
        #tabhome_layout.addLayout(menuBar_layout)
        tabhome_layout.addLayout(top_panel)
        tabhome.setLayout(tabhome_layout)

        # Thêm tab vào QTabWidget
        self.tab.addTab(tabhome, "Home")  # bạn có thể đổi tên tab
        self.tab.setStyleSheet("""QTabBar::tab { color: #2980b9;
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                    padding: 2px; 
                    }""")
        # Thêm tab 2 gồm 2 txt 4 btn
        tab2 = QWidget()
        tab2_layout = QHBoxLayout()# layout chính của tab2

        tab2_layouta = QVBoxLayout()#bên trái
        self.lblA=QLabel("A")
        self.btn_coppyA=QPushButton("CoppyA")
        self.btn_coppyA.setFixedSize(70,40)
        
        self.btn_resetA =QPushButton("ResetA")
        self.btn_resetA.setFixedSize(70,40)
        
        self.txtdatatab2A= QTextEdit()
        
        self.txtdatatab2A.setAcceptRichText(False)
        self.txtdatatab2A.setFixedWidth(250)
        tab2_layouta.addWidget(self.btn_coppyA)
        tab2_layouta.addWidget(self.lblA)
        tab2_layouta.addWidget(self.txtdatatab2A)
        tab2_layouta.addWidget(self.btn_resetA)

        tab2_layoutb = QHBoxLayout()#ở giữa
        tab2_layoutb.setContentsMargins(0, 150, 0, 0)  # đẩy toàn bộ cụm xuống khỏi đỉnh 50px

        tab2_layoutb1 = QVBoxLayout()

        
        tab2_layoutb1.setSpacing(30)         # giảm khoảng cách giữa các nút
        self.btnAB=QPushButton("'A','B'")
        self.btnAB.setFixedSize(70,40)
        
        self.btn_removedup = QPushButton("Remove \nduplicate")
        self.btn_removedup.setFixedSize(80,60)
        


        tab2_layoutb1.addWidget(self.btnAB)        
        tab2_layoutb1.addWidget(self.btn_removedup)
        tab2_layoutb1.addStretch()
        tab2_layoutb.addLayout(tab2_layoutb1)

        tab2_layoutc= QVBoxLayout()
        self.lblB=QLabel("B")
        self.btn_coppyB=QPushButton("CoppyB")
        self.btn_coppyB.setFixedSize(70,40)
       
        self.btn_resetB =QPushButton("ResetB")
        self.btn_resetB.setFixedSize(70,40)
        
        self.txtdatatab2B= QTextEdit()
        self.txtdatatab2B.setFixedWidth(250)
        self.txtdatatab2A.setAcceptRichText(False)

        
        tab2_layoutc.addWidget(self.btn_coppyB)
        tab2_layoutc.addWidget(self.lblB)
        tab2_layoutc.addWidget(self.txtdatatab2B)
        tab2_layoutc.addWidget(self.btn_resetB)

        tab2_layout.addLayout(tab2_layouta)
        tab2_layout.addLayout(tab2_layoutb)
        tab2_layout.addLayout(tab2_layoutc)
        tab2.setLayout(tab2_layout)       
        self.tab.addTab(tab2, "Text to sql")

        #set txt
        for txt in [self.txtdata_edit,self.txtdatatab2A,self.txtdatatab2B]:
            txt.setStyleSheet("""
        QTextEdit {
            border: 2px solid #3498db;
            border-radius: 8px;
            padding: 6px;
            background-color: #dcdcdc;
            font-size: 14px;
            font-family: Consolas;
        }
    """)
        for btn in [ self.btnselect,self.btnexcel,self.btnexit,self.btnclear,self.btn_removedup,self.btnAB,self.btn_coppyA,self.btn_coppyB,self.btn_resetA,self.btn_resetB]:
            btn.setStyleSheet("""
            QPushButton {
                              color: #2980b9;
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                background-color: #f0f0f0;      /* Xanh dương nhạt */
               
                border: 1px solid #7fb1cc;      /* Viền xanh dương hơi đậm */
                border-radius: 12px;             /* Bo góc */
                padding: 6px 12px;              /* Đệm trong nút */
            }

            QPushButton:hover {
                background-color: #bfe3f4;      /* Hiệu ứng khi rê chuột */
            }

            QPushButton:pressed {
                background-color: #91c9e8;      /* Hiệu ứng khi nhấn nút */
            }
        """)
        
        # Style cho group box
        for gb in [group_type, group_t]:
            gb.setStyleSheet("""
                QGroupBox {
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                    color: #1a237e;
                    border: 2px solid #3498db;
                    border-radius: 8px;
                    margin-top: 10px;
                }
                QGroupBox:title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
            """)

        for lbl in [self.lblA,self.lblB,self.lblcountedittxt,self.lbltablecount]:
            lbl.setStyleSheet("""
                QLabel {
                    color: #2980b9;
                    font-size: 12px;
                    font-family: Consolas;
                    font-weight: bold;
                    
                }
            """)

        #Layout chính chứa TabWidget
        layout_main = QVBoxLayout()
        layout_main.addWidget(self.tab)
        self.setLayout(layout_main)
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Main_gui()
    form.show()
    sys.exit(app.exec())


    