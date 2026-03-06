import os
import concurrent.futures

def xoa_file_don_le(duong_dan):
    """Hàm thực thi việc xoá 1 file và bắt lỗi nếu có."""
    try:
        os.remove(duong_dan)
        return 1  # Đánh dấu xoá thành công 1 file
    except Exception as e:
        print(f"Không thể xoá {duong_dan}. Lỗi: {e}")
        return 0

def xoa_asr_sieu_toc(thu_muc):
    # 1. Quét siêu tốc bằng os.scandir
    try:
        # os.scandir nhanh hơn pathlib và os.listdir vì nó lấy trực tiếp 
        # thông tin file từ cache của hệ điều hành, bỏ qua các lệnh gọi stat() thừa
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

    print(f"Đã tìm thấy {tong_so_file} file. Đang tiến hành xoá song song...")

    # 2. Xoá đa luồng (Multi-threading) để tối đa hoá tốc độ I/O
    # Thay vì đợi xoá xong file A mới xoá file B, script sẽ gửi lệnh xoá hàng loạt
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # executor.map sẽ phân bổ danh sách file cho các luồng xử lý cùng lúc
        ket_qua = executor.map(xoa_file_don_le, danh_sach_file)
        so_luong_da_xoa = sum(ket_qua)
        
    return so_luong_da_xoa

# --- Cách sử dụng ---
# ĐỔI ĐƯỜNG DẪN NÀY THÀNH THƯ MỤC CỦA BẠN
thu_muc_xu_ly = "./duong_dan_thu_muc_cua_ban" 

tong_da_xoa = xoa_asr_sieu_toc(thu_muc_xu_ly)
print(f"Hoàn tất! Tổng số file đã xoá thành công: {tong_da_xoa}")
