import os
import concurrent.futures
from tqdm import tqdm

def xoa_file_don_le(duong_dan):
    """Hàm thực thi việc xoá 1 file."""
    try:
        os.remove(duong_dan)
        return 1  # Xoá thành công
    except Exception as e:
        # Dùng tqdm.write thay vì print để không làm vỡ giao diện thanh tiến trình
        tqdm.write(f"Lỗi xoá {duong_dan}: {e}")
        return 0

def xoa_asr_co_progress_bar(thu_muc):
    # 1. Quét tìm file
    try:
        danh_sach_file = [
            entry.path for entry in os.scandir(thu_muc) 
            if entry.is_file() and entry.name.startswith("asr")
        ]
    except FileNotFoundError:
        print(f"Lỗi: Thư mục '{thu_muc}' không tồn tại.")
        return 0
    except PermissionError:
         print(f"Lỗi: Không có quyền truy cập thư mục '{thu_muc}'.")
         return 0

    tong_so_file = len(danh_sach_file)
    if tong_so_file == 0:
        print("Không tìm thấy file nào bắt đầu bằng 'asr' để xoá.")
        return 0

    print(f"Đã tìm thấy {tong_so_file} file. Bắt đầu tiến trình xoá...")
    so_luong_da_xoa = 0

    # 2. Xoá đa luồng kết hợp thanh tiến trình
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Gửi toàn bộ lệnh xoá vào hàng đợi
        futures = {executor.submit(xoa_file_don_le, path): path for path in danh_sach_file}
        
        # tqdm bọc quanh as_completed để theo dõi tiến độ các luồng
        for future in tqdm(concurrent.futures.as_completed(futures), total=tong_so_file, desc="Tiến độ xoá", unit=" file"):
            so_luong_da_xoa += future.result()
        
    return so_luong_da_xoa

# --- Cách sử dụng ---
thu_muc_xu_ly = "./duong_dan_thu_muc_cua_ban" 

tong_da_xoa = xoa_asr_co_progress_bar(thu_muc_xu_ly)
print(f"\nHoàn tất! Tổng số file đã xoá thành công: {tong_da_xoa}")
