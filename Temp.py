import json
import os
import glob

def normalize_text(value):
    """Chuẩn hóa dữ liệu đầu vào thành dạng chuỗi (string)."""
    if isinstance(value, list):
        if not value:
            return ""
        return "\n".join(str(v) for v in value)
    return str(value) if value is not None else ""

def extract_translation_pairs(data, current_path=None, extracted_data=None):
    """Duyệt đệ quy file JSON để trích xuất các cặp 'original' và 'localized'."""
    if current_path is None:
        current_path = []
    if extracted_data is None:
        extracted_data = []

    if isinstance(data, dict):
        if 'original' in data and 'localized' in data:
            extracted_data.append({
                'path': current_path.copy(),
                'original': normalize_text(data['original']),
                'localized': normalize_text(data['localized'])
            })
        
        for key, value in data.items():
            extract_translation_pairs(value, current_path + [key], extracted_data)
            
    elif isinstance(data, list):
        for index, item in enumerate(data):
            extract_translation_pairs(item, current_path + [index], extracted_data)

    return extracted_data

def update_json_with_evaluation(original_data, evaluated_data):
    """Chèn thêm 'score' và 'suggestion' vào JSON gốc dựa trên 'path'."""
    for item in evaluated_data:
        path = item['path']
        score = item.get('score')
        suggestion = item.get('suggestion')

        target = original_data
        for key in path:
            target = target[key]
            
        target['score'] = score
        target['suggestion'] = suggestion

    return original_data

def process_translation_folder(input_folder, output_folder):
    """
    Quét toàn bộ file .json trong thư mục đầu vào, xử lý và lưu sang thư mục đầu ra.
    """
    # 1. Tạo thư mục đầu ra nếu chưa tồn tại
    os.makedirs(output_folder, exist_ok=True)

    # 2. Tìm tất cả các file .json trong thư mục đầu vào
    search_pattern = os.path.join(input_folder, "*.json")
    json_files = glob.glob(search_pattern)

    if not json_files:
        print(f"⚠️ Không tìm thấy file .json nào trong thư mục: {input_folder}")
        return

    print(f"🔍 Tìm thấy {len(json_files)} file. Bắt đầu xử lý...\n")

    # 3. Duyệt qua từng file để xử lý
    for file_path in json_files:
        filename = os.path.basename(file_path)
        output_path = os.path.join(output_folder, filename)

        try:
            # Đọc file JSON gốc
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Trích xuất dữ liệu
            extracted = extract_translation_pairs(data)

            # ---------------------------------------------------------
            # [MÔ PHỎNG] BƯỚC GỌI LLM CHẤM ĐIỂM
            # Tại đây, bạn sẽ gọi API của LLM (ví dụ: OpenAI, Gemini)
            # truyền 'extracted' vào prompt và lấy kết quả trả về.
            for item in extracted:
                # Giả sử LLM trả về kết quả như sau:
                item['score'] = 8.5
                item['suggestion'] = f"Đã review bởi LLM."
            # ---------------------------------------------------------

            # Cập nhật lại dữ liệu với kết quả từ LLM
            updated_data = update_json_with_evaluation(data, extracted)

            # Ghi ra file JSON mới ở thư mục output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(updated_data, f, indent=4, ensure_ascii=False)

            print(f"✅ Thành công: {filename} (Xử lý {len(extracted)} node dịch)")

        except json.JSONDecodeError:
            print(f"❌ Lỗi: File {filename} không đúng định dạng JSON chuẩn.")
        except Exception as e:
            print(f"❌ Lỗi không xác định với file {filename}: {str(e)}")

    print(f"\n🎉 Hoàn tất! Các file đã xử lý được lưu tại: {output_folder}")

# ==========================================
# KHỞI CHẠY CHƯƠNG TRÌNH
# ==========================================
if __name__ == "__main__":
    # Khai báo đường dẫn thư mục. Bạn có thể thay đổi đường dẫn này.
    INPUT_DIR = "./input_jsons"
    OUTPUT_DIR = "./output_jsons"
    
    # Chạy hàm xử lý
    process_translation_folder(INPUT_DIR, OUTPUT_DIR)
