import pandas as pd

def process_tsv_list_pandas(tsv_files, separator=" "):
    result_list = []
    
    for file_path in tsv_files:
        try:
            # Đọc file tsv, chỉ load cột thứ 4 (usecols=[3]) để tối ưu bộ nhớ
            # header=None giả sử file của bạn không có dòng tiêu đề. Nếu có dòng tiêu đề, bạn có thể bỏ header=None đi.
            df = pd.read_csv(file_path, sep='\t', header=None, usecols=[3])
            
            # Chuyển cột thành list các string và nối lại
            joined_row = separator.join(df[3].astype(str).tolist())
            result_list.append(joined_row)
            
        except Exception as e:
            print(f"Lỗi khi xử lý {file_path}: {e}")
            
    return result_list

# --- Ví dụ cách sử dụng ---
my_tsv_files = ['file1.tsv', 'file2.tsv']
final_list_pd = process_tsv_list_pandas(my_tsv_files)
