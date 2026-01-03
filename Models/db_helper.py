import cx_Oracle
import pyodbc
from Models import globals
def orclquerry(sql):
    try:
        ora = globals.Oracle() 
        conn = cx_Oracle.connect(
            user=ora.user,
            password=ora.password,
            dsn=ora.dsn
        )
        print(f"Querying Oracle DB: {ora.db_name} at {ora.ip}")
        cursor = conn.cursor()
        cursor.execute(sql)

        headers = [desc[0].strip() for desc in cursor.description]  # loại bỏ khoảng trắng
        rows = cursor.fetchall()
        
        return headers, rows

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return [], []

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def orclquerry_extend(select , table , column ,listq,condition="",group_orderBy="",avc = True):
    try:
        ora = globals.Oracle() 
        conn = cx_Oracle.connect(
            user=ora.user,

            password=ora.password,
            dsn=ora.dsn
        )
        print(f"Querying Oracle DB: {ora.db_name} at {ora.ip}")
        list_new=split_list(listq,1000)
        sql ="select "+select +" from "+table +" where " 
        conditions  = [" "+column+" IN (" + ",".join(f"'{sn}'" for sn in group) + ")" for group in list_new]
        sql_where = " OR ".join(conditions)
        sql +=" "+ sql_where + " "+ condition + " "+group_orderBy
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)

        headers = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        conn.close()
        return headers, rows
    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return [], [] 
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

def split_list(list, chunk_size):
    for i in range(0, len(list), chunk_size):
        yield list[i:i + chunk_size]

def orcl_execute(sql):
    try:
        ora = globals.Oracle() 
        conn = cx_Oracle.connect(
            user=ora.user,
            password=ora.password,
            dsn=ora.dsn
        )
        print(f"Oracle DB: {ora.db_name} at {ora.ip}")
        cursor = conn.cursor()
        cursor.execute(sql)
        affected_rows = cursor.rowcount
        conn.commit()
        return affected_rows  # Trả về số dòng ảnh hưởng

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return -1  # Trả về -1 khi có lỗi

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass



def sqlquerry(sql):
    try:
        conn = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=10.120.15.117;"           
            r"UID=shopfloor;"
            r"PWD=happy123;"
            r"Trusted_Connection=no;"
        )
        cursor = conn.cursor()
        cursor.execute(sql)

        headers = [desc[0].strip() for desc in cursor.description]  # loại bỏ khoảng trắng
        rows = cursor.fetchall()
        
        return headers, rows

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return [], []

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def sqlquerry_extend(select , table , column ,listq,condition="",group_orderBy=""):
    try:
        conn = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=10.120.15.117;"           
            r"UID=shopfloor;"
            r"PWD=happy123;"
            r"Trusted_Connection=no;"
        )
        list_new=split_list(listq,1000)
        sql ="select "+select +" from "+table +" where " 
        conditions  = [" "+column+" IN (" + ",".join(f"'{sn}'" for sn in group) + ")" for group in list_new]
        sql_where = " OR ".join(conditions)
        sql +=" "+ sql_where + " "+ condition + " "+group_orderBy
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)

        headers = [desc[0].strip() for desc in cursor.description]  # loại bỏ khoảng trắng
        rows = cursor.fetchall()
        
        return headers, rows

    except cx_Oracle.DatabaseError as e:
        print("Database error:", e)
        return [], []

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


def sql_execute(sql):
    try:
        conn = pyodbc.connect(
            r"DRIVER={ODBC Driver 17 for SQL Server};"
            r"SERVER=10.120.15.117;"
            r"UID=shopfloor;"
            r"PWD=happy123;"
            r"Trusted_Connection=no;"
         )        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return cursor.rowcount  # ← Trả về số dòng bị xóa
    except pyodbc.Error as e:
        print("Lỗi khi xóa:", e)
        return 0
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass