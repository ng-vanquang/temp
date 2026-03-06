import os
import json
from tqdm import tqdm

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
# 2. XỬ LÝ THEO 3 BƯỚC (3 STEPS)
# ==========================================

def process_3_steps(input_folder, output_folder, target_keys):
    
    # Quét lấy danh sách file trước
    json_files = []
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".json"):
                json_files.append(os.path.join(root, filename))

    if not json_files:
        print(f"Không tìm thấy file .json nào trong '{input_folder}'")
        return

    # Dictionary lưu trữ toàn bộ dữ liệu in-memory
    master_data = {}

    print(f"Đã tìm thấy {len(json_files)} file. Bắt đầu pipeline 3 bước...\n")

    # ---------------------------------------------------------
    # BƯỚC 1: Đọc toàn bộ file và trích xuất dữ liệu vào Dict
    # ---------------------------------------------------------
    for input_filepath in tqdm(json_files, desc="Step 1: Đọc & Extract", unit="file"):
        root = os.path.dirname(input_filepath)
        filename = os.path.basename(input_filepath)
        
        # Tính toán đường dẫn output tương ứng
        rel_path = os.path.relpath(root, input_folder)
        target_dir = os.path.join(output_folder, rel_path)
        name, ext = os.path.splitext(filename)
        output_filepath = os.path.join(target_dir, f"{name}-translated{ext}")

        try:
            with open(input_filepath, 'r', encoding='utf-8') as file:
                json_data = json.load(file)

            extracted_items = extract_text_with_paths(json_data, target_keys)
            
            # Lưu mọi thứ vào bộ nhớ
            master_data[input_filepath] = {
                "output_filepath": output_filepath,
                "target_dir": target_dir,
                "json_data": json_data, # Giữ file gốc trong RAM để map lại ở Step 3
                "extracted_items": extracted_items,
                "translated_items": [] # Sẽ được điền ở Step 2
            }
        except Exception as e:
            tqdm.write(f"[LỖI ĐỌC FILE] {input_filepath}: {e}")

    # ---------------------------------------------------------
    # BƯỚC 2: Lặp qua Dict và tiến hành dịch thuật
    # ---------------------------------------------------------
    # Lưu ý: Lúc này ổ cứng hoàn toàn nghỉ ngơi, mọi thao tác diễn ra trên RAM
    for input_filepath, file_info in tqdm(master_data.items(), desc="Step 2: Dịch thuật", unit="file"):
        extracted_items = file_info["extracted_items"]
        
        if extracted_items:
            # Gửi dữ liệu đi dịch và lưu kết quả vào file_info
            file_info["translated_items"] = mock_translation_service(extracted_items)

    # ---------------------------------------------------------
    # BƯỚC 3: Lắp ráp bản dịch và Ghi ra file mới
    # ---------------------------------------------------------
    for input_filepath, file_info in tqdm(master_data.items(), desc="Step 3: Cập nhật & Ghi", unit="file"):
        try:
            # Tạo thư mục đích nếu chưa có
            os.makedirs(file_info["target_dir"], exist_ok=True)
            
            json_data = file_info["json_data"]
            translated_items = file_info["translated_items"]

            # Cập nhật JSON nếu có dữ liệu dịch
            if translated_items:
                updated_json_data = update_json_with_paths(json_data, translated_items)
            else:
                updated_json_data = json_data

            # Ghi ra đĩa
            with open(file_info["output_filepath"], 'w', encoding='utf-8') as file:
                json.dump(updated_json_data, file, ensure_ascii=False, indent=4)
                
        except Exception as e:
            tqdm.write(f"[LỖI GHI FILE] {file_info['output_filepath']}: {e}")


# ==========================================
# CHẠY THỰC TẾ
# ==========================================

if __name__ == "__main__":
    THU_MUC_INPUT = "input_json_files"
    THU_MUC_OUTPUT = "output_json_files"
    DANH_SACH_KEYS = ["request", "description", "title", "content"]

    process_3_steps(THU_MUC_INPUT, THU_MUC_OUTPUT, DANH_SACH_KEYS)
    print("\nHoàn tất toàn bộ quá trình!")
