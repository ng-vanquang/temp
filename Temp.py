import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# --- CẤU HÌNH ---
ID_FILE = 'id.txt'              # File chứa danh sách ID cần lọc
DATA_FILE = 'data.txt'          # File chứa: id \t đường_dẫn_audio
DEST_DIR = r'path/to/folder_B'  # Folder đích
OUTPUT_LIST = 'audiolist.txt'   # File kết quả (Sẽ đúng thứ tự như data.txt)
NUM_THREADS = 64                # Số luồng (SSD: 64-100, HDD: 16-32)
SOURCE_ROOT_DIR = r''           # Điền đường dẫn gốc nếu trong data.txt là đường dẫn tương đối

def load_target_ids(id_file_path):
    """Đọc file id.txt vào set để tra cứu cực nhanh O(1)"""
    print(f"Đang đọc ID từ {id_file_path}...")
    try:
        with open(id_file_path, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {id_file_path}")
        return set()

def copy_worker(task):
    """
    Hàm worker thực hiện copy.
    QUAN TRỌNG: Hàm này phải trả về kết quả (tên file hoặc None)
    để executor.map thu thập theo đúng thứ tự.
    """
    audio_id, raw_path = task
    
    # Xử lý đường dẫn
    if SOURCE_ROOT_DIR:
        src_path = os.path.join(SOURCE_ROOT_DIR, raw_path)
    else:
        src_path = raw_path

    filename = os.path.basename(src_path)
    dst_path = os.path.join(DEST_DIR, filename)

    try:
        if not os.path.exists(src_path):
            return None # File nguồn không tồn tại
        
        # Copy file
        shutil.copy2(src_path, dst_path)
        
        # Trả về tên file thành công
        return filename
    except Exception:
        return None # Lỗi khi copy

def main():
    # 1. Tạo thư mục đích
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    # 2. Load danh sách ID cần lọc
    target_ids = load_target_ids(ID_FILE)
    if not target_ids:
        print("Không có ID nào để xử lý.")
        return

    # 3. Quét data.txt để tạo danh sách công việc (Giữ nguyên thứ tự đọc)
    print(f"Đang đọc {DATA_FILE} để lọc file...")
    tasks = []
    
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            
            parts = line.split('\t')
            if len(parts) >= 2:
                curr_id = parts[0].strip()
                curr_path = parts[1].strip()
                
                # Chỉ thêm vào danh sách nếu ID nằm trong tập hợp cần lấy
                if curr_id in target_ids:
                    # Append vào list sẽ giữ nguyên thứ tự xuất hiện trong file
                    tasks.append((curr_id, curr_path))

    total_tasks = len(tasks)
    print(f"Tìm thấy {total_tasks} file cần copy. Bắt đầu xử lý đa luồng...")
    print("LƯU Ý: Tiến trình có thể khựng lại nếu gặp file lớn, nhưng thứ tự vẫn được đảm bảo.")

    # 4. Thực thi và ghi file
    with open(OUTPUT_LIST, 'w', encoding='utf-8') as f_out:
        
        with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
            # SỬ DỤNG executor.map THAY VÌ executor.submit
            # map trả về generator yield kết quả theo đúng thứ tự của tasks
            results = executor.map(copy_worker, tasks)
            
            # Duyệt qua kết quả từ map.
            # tqdm chỉ để hiện thanh tiến trình cho đẹp.
            for result_filename in tqdm(results, total=total_tasks, unit="file"):
                if result_filename:
                    f_out.write(result_filename + '\n')
    
    print(f"\nHOÀN TẤT!")
    print(f"Danh sách file đã lưu tại: {OUTPUT_LIST} (Đúng thứ tự gốc)")

if __name__ == "__main__":
    main()
