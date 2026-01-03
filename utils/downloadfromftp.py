import os
from ftplib import FTP

def download_from_ftp(host, user, password, list_remotepath, save_folder):
    os.makedirs(save_folder, exist_ok=True)
    downloaded_files = []

    try:
        with FTP(host) as ftp:
            ftp.login(user, password)
            print(f"✅ Đã kết nối FTP: {host}")

            for sn, ftp_path, group in list_remotepath:
                try:
                    # --- Tách đường dẫn và tên file ---
                    remote_dir = os.path.dirname(ftp_path)
                    filename = os.path.basename(ftp_path)

                    # --- Di chuyển vào đúng thư mục ---
                    ftp.cwd(remote_dir)

                    # --- Đường dẫn local ---
                    local_path = os.path.join(save_folder,group)
                    os.makedirs(local_path, exist_ok=True)
                    local_path = os.path.join(local_path, filename)
                    # --- Tải file ---
                    with open(local_path, "wb") as f:
                        ftp.retrbinary(f"RETR " + filename, f.write)

                    print(f"✅ Đã tải: {filename}")
                    downloaded_files.append(filename)
                    yield (sn,ftp_path,group,"ok")
                except Exception as e:
                    print(e)
                    yield (sn,ftp_path,group,"ng")
                    continue

        

    except Exception as e:
        print(f"❌ Không thể kết nối FTP: {e}")
        return None
