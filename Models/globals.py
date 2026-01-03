is_db = "AVC"  # Mặc định

class Oracle:
    def __init__(self, db_name=None):
        # Nếu không truyền, dùng giá trị toàn cục
        self.db_name = db_name or is_db  

        if self.db_name == "AVC":
            self.database = "avcsfge"
            self.ip = "10.120.15.10"
            self.user = "tbilly"
            self.password = "avc258"
            self.port = "1526"
        elif self.db_name == "CNC":
            self.database = "sfge"
            self.ip = "10.130.15.10"
            self.user = "txingxue"
            self.password = "jxx1214*"
            self.port = "1526"
        else:
            raise ValueError("Database không hợp lệ (chỉ được AVC hoặc CNC)")

        # Tạo DSN
        self.dsn = f"{self.ip}:{self.port}/{self.database}"


class sql_sever:
    def __init__(self, db_name=None):
        self.db_name = db_name or is_db  

        if self.db_name == "AVC":
            self.sever = "10.120.15.117"
        elif self.db_name == "CNC":
            self.sever = "10.130.15.117"
        else:
            raise ValueError("Database không hợp lệ (chỉ được AVC hoặc CNC)")


