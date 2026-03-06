from pathlib import Path

def dem_file_asr(thu_muc):
    # Khởi tạo đối tượng Path cho thư mục
    duong_dan = Path(thu_muc)
    
    # Kiểm tra xem đường dẫn có phải là thư mục hợp lệ không
    if not duong_dan.is_dir():
        print(f"Lỗi: '{thu_muc}' không tồn tại hoặc không phải là thư mục.")
        return 0

    # Lọc các mục bắt đầu bằng 'asr' và đếm nếu mục đó là file (bỏ qua thư mục)
    so_luong = sum(1 for file in duong_dan.glob("asr*") if file.is_file())
    
    return so_luong

# --- Cách sử dụng ---
# Thay đổi biến dưới đây thành đường dẫn thư mục thực tế trên máy của bạn
thu_muc_can_kiem_tra = "./duong_dan_thu_muc_cua_ban" 
tong_so = dem_file_asr(thu_muc_can_kiem_tra)

print(f"Tổng số file bắt đầu bằng 'asr' là: {tong_so}")
