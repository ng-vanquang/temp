def update_json_with_paths(original_data, translated_items):
    """
    Hàm đắp bản dịch vào lại JSON gốc dựa trên đường dẫn (path).
    
    :param original_data: Object JSON gốc (sẽ bị thay đổi trực tiếp).
    :param translated_items: Danh sách các dict chứa 'path' và 'trans_text'.
    :return: Object JSON đã được cập nhật bản dịch.
    """
    for item in translated_items:
        path = item.get("path")
        trans_text = item.get("trans_text")
        
        # Bỏ qua nếu dữ liệu không hợp lệ
        if not path or trans_text is None:
            continue

        # Dùng một biến con trỏ để đi sâu vào cấu trúc JSON
        current_node = original_data
        
        # Duyệt path từ đầu đến phần tử áp chót (bỏ qua phần tử cuối cùng)
        for key_or_index in path[:-1]:
            current_node = current_node[key_or_index]
            
        # Phần tử cuối cùng trong path chính là key/index cần thay thế
        final_key = path[-1]
        
        # Gán đè bản dịch vào đúng vị trí
        current_node[final_key] = trans_text

    return original_data

# ==========================================
# CHẠY THỬ NGHIỆM VỚI DỮ LIỆU ĐÃ DỊCH
# ==========================================

# 1. Mock data gốc (tương tự như bước trước)
mock_json_data = {
    "metadata": {
        "description": "Đây là mô tả chung của file"
    },
    "data_list": [
        {
            "id": 101,
            "request": "Yêu cầu số 1",
            "details": {
                "description": "Mô tả chi tiết yêu cầu 1"
            }
        }
    ]
}

# 2. Giả lập data bạn đã xử lý xong phần dịch (có path và trans_text)
danh_sach_da_dich = [
  {
    "path": ["metadata", "description"],
    "trans_text": "This is the general description of the file"
  },
  {
    "path": ["data_list", 0, "request"],
    "trans_text": "Request number 1"
  },
  {
    "path": ["data_list", 0, "details", "description"],
    "trans_text": "Detailed description of request 1"
  }
]

# 3. Chạy hàm cập nhật
json_hoan_thien = update_json_with_paths(mock_json_data, danh_sach_da_dich)

# In kết quả kiểm tra
import json
print(json.dumps(json_hoan_thien, ensure_ascii=False, indent=2))
