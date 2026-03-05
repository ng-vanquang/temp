import os
import json
from tqdm import tqdm # Import thư viện progress bar

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
# 2. XỬ LÝ VỚI PROGRESS BAR
# ==========================================

def process_nested_json_folders(input_folder, output_folder, target_keys):
    """
    Duyệt đệ quy, giữ nguyên cấu trúc, đổi tên file và hiển thị progress bar.
    """
    # 1. Quét trước để thu thập tất cả đường dẫn file JSON
    json_files = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".json"):
                json_files.append(os.path.join(root, filename))

    if not json_files:
        print(f"Không tìm thấy file .json nào trong thư mục '{input_folder}'")
        return

    print(f"Tìm thấy tổng cộng {len(json_files)} file JSON. Bắt đầu xử lý...\n")

    # 2. Xử lý từng file kết hợp Progress Bar
    # Sử dụng tqdm bao bọc danh sách file để tạo thanh tiến trình
    for input_filepath in tqdm(json_files, desc="Tiến độ dịch thuật", unit="file"):
        
        # Tách root và filename từ input_filepath
        root = os.path.dirname(input_filepath)
        filename = os.path.basename(input_filepath)

        # Tính toán đường dẫn tương đối và tạo thư mục đích
        rel_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, rel_path)
        os.makedirs(target_dir, exist_ok=True)

        # Đổi tên file
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}-translated{ext}"
        output_filepath = os.path.join(target_dir, new_filename)
        
        try:
            # Xử lý lõi
            with open(input_filepath, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            extracted_items = extract_text_with_paths(json_data, target_keys)
            
            # Nếu file không có key nào cần dịch, ta vẫn có thể copy sang folder mới
            if extracted_items:
                translated_items = mock_translation_service(extracted_items)
                updated_json_data = update_json_with_paths(json_data, translated_items)
            else:
                updated_json_data = json_data # Giữ nguyên nếu không có gì để dịch

            with open(output_filepath, 'w', encoding='utf-8') as file:
                json.dump(updated_json_data, file, ensure_ascii=False, indent=4)

        except Exception as e:
            # Lưu ý: Khi dùng tqdm, dùng tqdm.write thay vì print để không làm vỡ giao diện thanh tiến trình
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
