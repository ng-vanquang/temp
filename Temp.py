import pandas as pd

def export_to_excel(index_file, data_file, output_file):
    # Đọc dữ liệu từ 2 file
    with open(index_file, 'r', encoding='utf-8') as f_idx:
        indices = [line.strip() for line in f_idx if line.strip()]
    
    with open(data_file, 'r', encoding='utf-8') as f_data:
        data_lines = [line.strip() for line in f_data if line.strip()]

    # Kiểm tra tính tương thích
    if len(indices) != len(data_lines):
        print("Cảnh báo: Số lượng dòng giữa 2 file không khớp!")
        return

    # Tạo DataFrame
    df = pd.DataFrame({
        'Index': indices,
        'Data': data_lines
    })

    # Nhóm các dòng có cùng Index lại với nhau
    # Ở đây mình nối các dòng Data cùng index bằng dấu phẩy
    grouped = df.groupby('Index')['Data'].apply(lambda x: ', '.join(x)).reset_index()

    # Xuất ra file Excel
    grouped.to_excel(output_file, index=False)
    print(f"Đã xuất thành công ra file: {output_file}")

# Sử dụng hàm
export_to_excel('index.txt', 'data.txt', 'ket_qua.xlsx')
