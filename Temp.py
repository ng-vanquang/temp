import os
import json

# ==========================================
# 1. CÁC HÀM XỬ LÝ LÕI (Giữ nguyên)
# ==========================================

def extract_text_with_paths(data, target_keys, current_path=None, extracted_items=None):
    if current_path is None: current_path = []
    if extracted_items is None: extracted_items = []

    if isinstance(data, dict):
        for key, value in data.items():
            new_path = current_path + [key]
            if key in target_keys and isinstance(value, str):
                extracted_items.append({"path": new_path, "original_text": value})
            if isinstance(value, (dict, list)):
                extract_text_with_paths(value, target_keys, new_path, extracted_items)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = current_path + [index]
            if isinstance(item, (dict, list)):
                extract_text_with_paths(item, target_keys, new_path, extracted_items)
    return extracted_items

def update_json_with_paths(original_data, translated_items):
    for item in translated_items:
        path = item.get("path")
        trans_text = item.get("trans_text")
        if not path or trans_text is None: continue
        
        current_node = original_data
        for key_or_index in path[:-1]:
            current_node = current_node[key_or_index]
            
        final_key = path[-1]
        current_node[final_key] = trans_text
    return original_data

def mock_translation_service(extracted_items):
    translated_items = []
    for item in extracted_items:
        translated_items.append({
            "path": item["path"],
            "trans_text": f"[ĐÃ DỊCH] {item['original_text']}"
        })
    return translated_items

# ==========================================
# 2. XỬ LÝ CÂY THƯ MỤC LỒNG NHAU (MỚI)
# ==========================================

def process_nested_json_folders(input_folder, output_folder, target_keys):
    """
    Duyệt đệ quy toàn bộ thư mục input, giữ nguyên cấu trúc khi lưu sang output,
    và thêm hậu tố '-translated' vào tên file json.
    """
    # Hàm os.walk sẽ đi qua từng thư mục, thư mục con, và lấy ra danh sách file
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".json"):
                # 1. Lấy đường dẫn tuyệt đối của file input
                input_filepath = os.path.join(root, filename)

                # 2. Tính toán đường dẫn tương đối (để clone cấu trúc thư mục)
                # Ví dụ: root là "input_folder/sub1/sub2" -> rel_path là "sub1/sub2"
                rel_path = os.path.relpath(root, input_folder)
                
                # 3. Tạo thư mục đích tương ứng bên trong output_folder
                target_dir = os.path.join(output_folder, rel_path)
                os.makedirs(target_dir, exist_ok=True) # exist_ok=True giúp không báo lỗi nếu thư mục đã có

                # 4. Tách tên file và đuôi file để thêm hậu tố "-translated"
                # Ví dụ: "data.json" -> name="data", ext=".json"
                name, ext = os.path.splitext(filename)
                new_filename = f"{name}-translated{ext}"
                
                # 5. Lắp ráp đường dẫn file output cuối cùng
                output_filepath = os.path.join(target_dir, new_filename)

                print(f"Đang xử lý: {input_filepath}")
                
                try:
                    # ĐỌC - TRÍCH XUẤT - DỊCH - CẬP NHẬT - GHI
                    with open(input_filepath, 'r', encoding='utf-8') as file:
                        json_data = json.load(file)

                    extracted_items = extract_text_with_paths(json_data, target_keys)
                    translated_items = mock_translation_service(extracted_items)
                    updated_json_data = update_json_with_paths(json_data, translated_items)

                    with open(output_filepath, 'w', encoding='utf-8') as file:
                        json.dump(updated_json_data, file, ensure_ascii=False, indent=4)
                        
                    print(f"  -> Lưu thành công: {output_filepath}")

                except Exception as e:
                    print(f"  -> [LỖI] Không thể xử lý file {input_filepath}: {e}")

# ==========================================
# CHẠY THỰC TẾ
# ==========================================

if __name__ == "__main__":
    THU_MUC_INPUT = "input_json_files"
    THU_MUC_OUTPUT = "output_json_files"
    DANH_SACH_KEYS = ["request", "description", "title", "content"]

    process_nested_json_folders(THU_MUC_INPUT, THU_MUC_OUTPUT, DANH_SACH_KEYS)
    print("\nHoàn tất toàn bộ quá trình!")
