from PySide6.QtCore import QObject, Signal
import os, glob
from PySide6.QtWidgets import QApplication
from Models import db_helper
import os
import glob
from utils import coppy_cal , downloadfromftp

class CoppyLogWorker(QObject):
    progress = Signal(str)
    result_file = Signal(str)
    result_ng = Signal(str)
    finished = Signal()

    def __init__(self, view, avc_db):
        super().__init__()
        self.view = view
        self.avc_db = avc_db

    def run_coppy_log(self):
        self.progress.emit("Go....")
        txtdata = self.view.txtdata.toPlainText()
        group = self.view.txtgroup.text()
        condition = ""
        sqlcondition = ""
        if group:
            condition = f" and GROUP_NAME='{group}'"
            sqlcondition = f" AND GROPU_NAME='{group}'"
        lines = []
        seen = set()

        for line in txtdata.splitlines():
            line = line.strip().upper()
            if line and line not in seen:
                seen.add(line)
                lines.append(line)
        list_sn_ftp = []
        headers, rows = db_helper.sqlquerry_extend(" FTP_FOLDER +'/'+ FTP_FILE as FTP_Path,LOG_SN,GROPU_NAME","TEST_LOG_100..LOCAL_TEST_LOG" , "LOG_SN", lines, sqlcondition)
        list_ftp_paths = []
        for row in rows:
            rowdict = dict(zip(headers, row))
            sn = rowdict["LOG_SN"]
            list_sn_ftp.append(sn)
            group = rowdict["GROPU_NAME"]
            ftp_path = rowdict["FTP_Path"].replace("ftp://10.120.15.34","") if rowdict["FTP_Path"] else ""
            list_ftp_paths.append((sn,ftp_path , group))
        
        list_sn_ok=[]
        for sn ,filename,group_rs, status in downloadfromftp.download_from_ftp(
        "10.120.15.34",
        "cncuser",
        "cnc%1234",
        list_ftp_paths,
        self.view.txtcoppyto.text()):
            if status=="ok":                
                self.result_file.emit((filename)) 
                list_sn_ok.append((sn,group_rs))           

        headers, rows = db_helper.orclquerry_extend(
            "distinct serial_number,key_part_no,mo_no,group_name",
            "sfism4.u_1a2a_yield_t",
            "SERIAL_NUMBER", lines, condition, " order by SERIAL_NUMBER", self.avc_db)
        group = self.view.txtgroup.text()
        for row in rows:            
            rowdict = dict(zip(headers, row))
            sn = rowdict["SERIAL_NUMBER"]
            model = rowdict["KEY_PART_NO"]
            mo = rowdict["MO_NO"]
            if not self.view.txtgroup.text():
                group = rowdict["GROUP_NAME"]
            if (sn,group)  in list_sn_ok:
                continue
            txtpath = self.view.txtpathfrom.toPlainText()
            path_lines = [line.strip() for line in txtpath.splitlines() if line]
            isFound = False
            print(sn , model, mo, group)
            for path_line in path_lines:
                path = os.path.join(path_line, model[3:5], model, group, mo, sn + "*")
                all_files = glob.glob(path)
                if all_files:
                    for file in all_files:
                        print(file)
                        pathto = os.path.join(self.view.txtcoppyto.text(), group)
                        coppy_cal.FileCopier.coppyfile_to(file, pathto)
                        self.result_file.emit(file)
                        isFound = True
                        QApplication.processEvents()
                    if isFound:
                        break
                else:
                    print("Not found path:", path)
                QApplication.processEvents()
            if not isFound:
                self.result_ng.emit(f"{sn}_{group}_{mo}")
            QApplication.processEvents()

        set_sn = {row[0] for row in rows}
        for line in lines:
            if line not in set_sn:
                self.result_ng.emit(f"{line}")
            QApplication.processEvents()

        self.progress.emit("Go")
        self.finished.emit()


    def run_coppy_cal(self):
        self.progress.emit("Go....")
        txtdata = self.view.txtdata.toPlainText()
        lines = [line.strip().upper() for line in txtdata.splitlines()if  line]        
        for line in lines:
            print(line)
            txtpath = self.view.txtpathfrom.toPlainText()
            path_lines= [line.strip() for line in txtpath.splitlines()if  line]  
            isFound=False 
            for  path_line in path_lines:
                path = os.path.join(path_line,line[0:len(line)-4],line+"*")
                print(path)
                all_files=glob.glob(path)
                if all_files:
                    for file in all_files:
                        print(file)
                        pathto = self.view.txtcoppyto.text()
                        coppy_cal.FileCopier.coppyfile_to(file,pathto)
                        self.result_file.emit(file)
                        isFound=True
                
            if not isFound:
                self.result_ng.emit(line)
            QApplication.processEvents()        
        self.progress.emit("Go")
        self.finished.emit()


