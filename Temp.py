def extract_text_with_paths(data, target_keys, current_path=None, extracted_items=None):
    """
    Hàm đệ quy trích xuất text từ JSON dựa trên danh sách key cho trước.
    
    :param data: Object JSON hiện tại (dict hoặc list).
    :param target_keys: Danh sách các key cần dịch (list of strings).
    :param current_path: Đường dẫn hiện tại đang duyệt (list).
    :param extracted_items: Danh sách lưu trữ kết quả (list of dicts).
    :return: Danh sách các object chứa đường dẫn (path) và nội dung (text).
    """
    # Khởi tạo giá trị mặc định cho lần gọi đầu tiên
    if current_path is None:
        current_path = []
    if extracted_items is None:
        extracted_items = []

    # Xử lý nếu data là một Object (Dictionary)
    if isinstance(data, dict):
        for key, value in data.items():
            # Tạo đường dẫn mới đến node hiện tại
            new_path = current_path + [key]
            
            # Nếu key nằm trong danh sách cần dịch và value là text
            if key in target_keys and isinstance(value, str):
                extracted_items.append({
                    "path": new_path,
                    "original_text": value
                })
            
            # Kể cả khi đã khớp hay không, nếu value chứa dữ liệu lồng nhau thì tiếp tục đi xuống
            if isinstance(value, (dict, list)):
                extract_text_with_paths(value, target_keys, new_path, extracted_items)

    # Xử lý nếu data là một Mảng (List)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = current_path + [index]
            # Mảng thì không có key, chỉ cần duyệt tiếp các phần tử bên trong
            if isinstance(item, (dict, list)):
                extract_text_with_paths(item, target_keys, new_path, extracted_items)

    return extracted_items


# ==========================================
# CHẠY THỬ NGHIỆM VỚI DỮ LIỆU ĐA DẠNG
# ==========================================

# Mock data mô phỏng cấu trúc phức tạp: mảng lồng object, object lồng mảng, 
# có key lặp lại, có key bị thiếu.
mock_json_data = {
    "metadata": {
        "version": 1.0,
        "description": "Đây là mô tả chung của file" # Cần dịch
    },
    "data_list": [
        {
            "id": 101,
            "request": "Yêu cầu số 1", # Cần dịch
            "details": {
                "description": "Mô tả chi tiết yêu cầu 1", # Cần dịch
                "notes": "Ghi chú không cần dịch"
            }
        },
        {
            "id": 102,
            # Thiếu key "request" và "description" ở đây (code vẫn chạy bình thường)
            "other_field": "Dữ liệu khác"
        }
    ]
}

keys_can_dich = ["request", "description"]

# Chạy hàm trích xuất
ket_qua_trich_xuat = extract_text_with_paths(mock_json_data, keys_can_dich)

# In kết quả
import json
print(json.dumps(ket_qua_trich_xuat, ensure_ascii=False, indent=2))
