import os
import json
from tqdm import tqdm

# ==========================================
# 1. CÁC HÀM XỬ LÝ LÕI
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
        original_text = item.get("original_text") # <--- Lấy original_text từ kết quả dịch
        
        if not path or trans_text is None: continue
        
        current_node = original_data
        # Đi sâu vào node áp chót
        for key_or_index in path[:-1]:
            current_node = current_node[key_or_index]
            
        final_key = path[-1] # Đây chính là tên key gốc (ví dụ: "request", "description")
        
        # 1. Thay thế text tại key hiện tại bằng bản dịch
        current_node[final_key] = trans_text
        
        # 2. Tạo một key mới cùng cấp để lưu text gốc
        # Bạn có thể đổi format tên key ở đây tùy ý (ví dụ: f"{final_key}_original")
        new_original_key = f"original_{final_key}"
        current_node[new_original_key] = original_text

    return original_data

def mock_translation_service(extracted_items):
    translated_items = []
    for item in extracted_items:
        translated_items.append({
            "path": item["path"],
            "trans_text": f"[ĐÃ DỊCH] {item['original_text']}",
            "original_text": item['original_text'] # <--- Trả về thêm original_text
        })
    return translated_items

# ==========================================
# 2. XỬ LÝ FILE (Giữ nguyên phiên bản dùng tqdm)
# ==========================================

def process_nested_json_folders(input_folder, output_folder, target_keys):
    json_files = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".json"):
                json_files.append(os.path.join(root, filename))

    if not json_files:
        print(f"Không tìm thấy file .json nào trong thư mục '{input_folder}'")
        return

    print(f"Tìm thấy tổng cộng {len(json_files)} file JSON. Bắt đầu xử lý...\n")

    for input_filepath in tqdm(json_files, desc="Tiến độ dịch thuật", unit="file"):
        root = os.path.dirname(input_filepath)
        filename = os.path.basename(input_filepath)

        rel_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        name, ext = os.path.splitext(filename)
        new_filename = f"{name}-translated{ext}"
        output_filepath = os.path.join(target_dir, new_filename)
        
        try:
            with open(input_filepath, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            extracted_items = extract_text_with_paths(json_data, target_keys)
            
            if extracted_items:
                translated_items = mock_translation_service(extracted_items)
                updated_json_data = update_json_with_paths(json_data, translated_items)
            else:
                updated_json_data = json_data

            with open(output_filepath, 'w', encoding='utf-8') as file:
                json.dump(updated_json_data, file, ensure_ascii=False, indent=4)

        except Exception as e:
            tqdm.write(f"[LỖI] Không thể xử lý file {input_filepath}: {e}")

# ==========================================
# CHẠY THỰC TẾ
# ==========================================

if __name__ == "__main__":
    THU_MUC_INPUT = "input_json_files"
    THU_MUC_OUTPUT = "output_json_files"
    DANH_SACH_KEYS = ["request", "description", "title", "content"]

    process_nested_json_folders(THU_MUC_INPUT, THU_MUC_OUTPUT, DANH_SACH_KEYS)
    print("\nHoàn tất toàn bộ quá trình!")
