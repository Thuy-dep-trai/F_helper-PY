import sys
from Controler import main_controler
from PySide6.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow
import sys
from View import Main_gui
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu,  QMessageBox
)
from PySide6.QtGui import QAction,QIcon
import os
from PySide6.QtCore import Qt
from Controler.label_reprint_ctrl import Label_reprint_controler
from Controler.update_weight_ctr import update_w_controler
from Controler.Coppy_log_ctrl import Coppy_log_ctrl
from Controler.Un_imei_ctrl import Un_imei_ctrl
from Controler.main_controler import Main_controler
from Controler.update_Mo_ctrl import update_Mo_ctrl
from Models import globals

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("F")
        self.resize(1320, 720)
        icon_path = os.path.join( "material","icomain.ico")
        self.setWindowIcon(QIcon(icon_path))       
        

        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)

        self.ctrl_coppylog = None  # lưu lại controller
        self.ctrl_labelreprint = None
        self.ctrl_updatew = None
        self.ctrl_unimei = None
        self.ctrl_main = None
        self.ctrl_update_mo = None

        self.menuItemTrip_home_do()

        

    # Tạo menu bar
        menu_bar = self.menuBar()  # ← Tự động nằm trên QMainWindow

        # Tạo menu File
        file_menu = menu_bar.addMenu("Menu")

        Label_reprint_action = QAction("Label_reprint", self)
        Label_reprint_action.triggered.connect(self.menuItemTrip_labelreprint_do)
        file_menu.addAction(Label_reprint_action)

        Update_w_action = QAction("Update_w", self)
        Update_w_action.triggered.connect(self.menuItemTrip_update_weight_do)
        file_menu.addAction(Update_w_action)

        CoppyLog_action = QAction("CoppyLog", self)
        CoppyLog_action.triggered.connect(self.menuItemTrip_CoppyLog_do)
        file_menu.addAction(CoppyLog_action)

        Unimei_action = QAction("Unimei", self)
        Unimei_action.triggered.connect(self.menuItemTrip_unimei_do)
        file_menu.addAction(Unimei_action)

        update_mo_action = QAction("Update_Mo", self)
        update_mo_action.triggered.connect(self.menuItemTrip_update_mo)
        file_menu.addAction(update_mo_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Tạo menu Edit
        Home_menu = menu_bar.addMenu("Home")

        home_action = QAction("Go to Home", self)
        home_action.triggered.connect(self.menuItemTrip_home_do)

        Home_menu.addAction(home_action)


        # Tạo menu Help
        db_menu = menu_bar.addMenu("database")
        self.AVC_action = QAction("AVC", self, checkable=True)
        self.AVC_action.setChecked(True)  # Mặc định chọn AVC
        self.CNC_action = QAction("CNC", self, checkable=True)
         # Kết nối sự kiện click
        self.AVC_action.triggered.connect(self.on_action_clicked)
        self.CNC_action.triggered.connect(self.on_action_clicked)
        db_menu.addAction(self.AVC_action)
        db_menu.addAction(self.CNC_action)

        # Tạo menu Help
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def on_action_clicked(self, checked):
        sender = self.sender()
        if sender == self.AVC_action and checked:
            self.CNC_action.setChecked(False)
        elif sender == self.CNC_action and checked:
            self.AVC_action.setChecked(False)
        elif not checked:
            sender.setChecked(True)  # Không cho bỏ chọn cả hai
            checked = True  # Giữ nguyên trạng thái checked
        globals.is_db = sender.text()
    def menuItemTrip_home_do(self):
        print("Home")
        try:
            # mở 1 from khác
            if self.ctrl_main is None or self.ctrl_main.view.parent() is None: 
                raise RuntimeError
        except RuntimeError:
                # Nếu không có controller hoặc widget đã bị xóa, tạo mới            
                self.ctrl_main=Main_controler()
        self.open_gui(self.ctrl_main.view)

    def menuItemTrip_labelreprint_do(self):
        print("label reprint")
        # mở 1 from khác
        try:
            if self.ctrl_labelreprint is None or self.ctrl_labelreprint.view.parent() is None : 
                raise RuntimeError
        except RuntimeError:
                # Nếu không có controller hoặc widget đã bị xóa, tạo mới
                self.ctrl_labelreprint=Label_reprint_controler()
        
        self.open_gui(self.ctrl_labelreprint.view)
    
    def menuItemTrip_unimei_do(self):
        print("unimei open")  
        try:            
            # Nếu không có controller hoặc widget đã bị xóa, tạo mới
            if self.ctrl_unimei is None or self.ctrl_unimei.view.parent() is None: 
                raise RuntimeError
        except RuntimeError:
                self.ctrl_unimei=Un_imei_ctrl()
        self.open_gui(self.ctrl_unimei.view)

    def menuItemTrip_update_weight_do(self):
        print("update weight") 
        try:  
            if self.ctrl_updatew is None or self.ctrl_updatew.view.parent() is None:
                raise RuntimeError
        except RuntimeError:
                # Nếu không có controller hoặc widget đã bị xóa, tạo mới   
                self.ctrl_updatew=update_w_controler()
        self.open_gui(self.ctrl_updatew.view)

    def menuItemTrip_CoppyLog_do(self):
        print("coppy log")  
        try:
            if self.ctrl_coppylog is None or self.ctrl_coppylog.view.parent() is None:
                raise RuntimeError
        except RuntimeError:
                self.ctrl_coppylog = Coppy_log_ctrl()
        self.open_gui(self.ctrl_coppylog.view)

    def menuItemTrip_update_mo(self):
        print("update mo")
        try:
            if self.ctrl_update_mo is None or self.ctrl_update_mo.view.parent() is None:
                raise RuntimeError
        except RuntimeError:
            self.ctrl_update_mo = update_Mo_ctrl()  # Luôn tạo mới nếu view bị xoá

        self.open_gui(self.ctrl_update_mo.view)

    
    
    def open_gui(self, child_widget):
        # Kiểm tra nếu form con đã được mở
        for sub in self.mdi_area.subWindowList():
            if isinstance(sub.widget(), child_widget.__class__):
                sub.widget().setFocus()
                sub.raise_()
                return  # Đã mở rồi thì không làm gì cả

        

        for sub in self.mdi_area.subWindowList():
            if sub.widget().__class__ == child_widget.__class__:
                sub.widget().setFocus()
                return
        sub = QMdiSubWindow()
        sub.setWidget(child_widget)
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.setWindowFlags(Qt.SubWindow)
        self.mdi_area.addSubWindow(sub)
        sub.showMaximized()
        sub.show()
        sub.widget().setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec()
    print("exit")