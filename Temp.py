import pandas as pd

def export_to_excel(index_file, data_file, output_file):
    # Đọc dữ liệu
    with open(index_file, 'r', encoding='utf-8') as f_idx:
        indices = [line.strip() for line in f_idx if line.strip()]
    
    with open(data_file, 'r', encoding='utf-8') as f_data:
        data_lines = [line.strip() for line in f_data if line.strip()]

    if len(indices) != len(data_lines):
        print("Cảnh báo: Số lượng dòng giữa 2 file không khớp!")
        return

    df = pd.DataFrame({'Index': indices, 'Data': data_lines})

    # Gom nhóm và nối bằng xuống dòng (\n)
    grouped = df.groupby('Index')['Data'].apply(lambda x: '\n'.join(x)).reset_index()

    # Xuất ra file Excel với định dạng đặc biệt để hỗ trợ xuống dòng
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    grouped.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Lấy workbook và worksheet để bật tính năng Wrap Text
    workbook = writer.book
    worksheet = workbook['Sheet1']
    
    # Bật Wrap Text cho cột chứa Data (cột B, index=1)
    for row in range(2, len(grouped) + 2):
        cell = worksheet.cell(row=row, column=2)
        cell.alignment = cell.alignment.copy(wrapText=True)
    
    writer.close()
    print(f"Đã xuất thành công ra file: {output_file}")

# Sử dụng hàm
export_to_excel('index.txt', 'data.txt', 'ket_qua.xlsx')
