import os
import json

def has_low_score(data, threshold=2.0):
    """
    Hàm đệ quy kiểm tra xem trong file JSON có bất kỳ node nào
    có key 'score' với giá trị <= threshold hay không.
    """
    if isinstance(data, dict):
        # Kiểm tra nếu dict hiện tại có trường 'score'
        if 'score' in data:
            try:
                # Ép kiểu về float để so sánh an toàn (đề phòng LLM trả về dạng string "2.0")
                score_value = float(data['score'])
                if score_value <= threshold:
                    return True  # Dừng tìm kiếm nhánh này, báo là có điểm thấp
            except (ValueError, TypeError):
                pass # Bỏ qua nếu score bị lỗi định dạng không thể chuyển thành số
        
        # Nếu chưa tìm thấy, tiếp tục lặn sâu vào các value của dict
        for key, value in data.items():
            if has_low_score(value, threshold):
                return True
                
    elif isinstance(data, list):
        # Duyệt qua các phần tử trong list
        for item in data:
            if has_low_score(item, threshold):
                return True
                
    return False

def find_low_score_files(output_folder, log_file_path, threshold=2.0):
    """
    Quét toàn bộ thư mục và ghi đường dẫn các file có điểm thấp ra file txt.
    """
    low_score_files = []

    print(f"🔍 Đang quét thư mục: {output_folder} ...")
    
    # os.walk giúp quét đệ quy tất cả các thư mục con bên trong
    for root, dirs, files in os.walk(output_folder):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        
                    # Nếu phát hiện điểm thấp, thêm đường dẫn vào danh sách
                    if has_low_score(data, threshold):
                        low_score_files.append(file_path)
                        
                except Exception as e:
                    print(f"❌ Lỗi khi đọc file {file_path}: {e}")

    # Ghi danh sách đường dẫn ra file .txt
    try:
        with open(log_file_path, 'w', encoding='utf-8') as log_file:
            for path in low_score_files:
                log_file.write(path + '\n')
        
        print(f"\n✅ Hoàn tất! Đã tìm thấy {len(low_score_files)} file có score <= {threshold}.")
        print(f"📁 Danh sách được lưu tại: {log_file_path}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file log: {e}")

# ==========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    # Đường dẫn tới thư mục output chứa các file JSON đã được LLM chấm điểm
    OUTPUT_DIR = "./output_jsons"  # Hãy thay đổi đường dẫn này cho khớp với thư mục của bạn
    
    # Đường dẫn file txt dùng để lưu kết quả
    LOG_FILE = "./danh_sach_file_diem_thap.txt"
    
    # Mức điểm cần lọc (<= 2)
    THRESHOLD = 2.0 
    
    # Chạy hàm quét
    find_low_score_files(OUTPUT_DIR, LOG_FILE, THRESHOLD)
