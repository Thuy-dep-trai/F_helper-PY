import os
import shutil

class FileCopier:
    @staticmethod
    def coppyfile_to(file_path,dest_folder):
        if os.path.exists(file_path):
            try:
                os.makedirs(dest_folder, exist_ok=True)
                file_name = os.path.basename(file_path)
                dest_path = os.path.join(dest_folder, file_name)
                shutil.copy(file_path, dest_path)
                return True
            except Exception as e:
                print(f"Lỗi khi copy file: {e}")
                return False
        else:
            print("Không tìm thấy file nguồn:", file_path)
            return False