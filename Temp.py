import pandas as pd
from collections import OrderedDict

def export_to_excel_ordered(index_file, data_file, output_file):
    # Đọc dữ liệu từ 2 file
    with open(index_file, 'r', encoding='utf-8') as f_idx:
        indices = [line.strip() for line in f_idx if line.strip()]
    
    with open(data_file, 'r', encoding='utf-8') as f_data:
        data_lines = [line.strip() for line in f_data if line.strip()]

    if len(indices) != len(data_lines):
        print("Cảnh báo: Số lượng dòng giữa 2 file không khớp!")
        return

    # Sử dụng OrderedDict để lưu trữ dữ liệu theo thứ tự xuất hiện lần đầu của Index
    data_dict = OrderedDict()
    
    for idx, val in zip(indices, data_lines):
        if idx not in data_dict:
            data_dict[idx] = val
        else:
            data_dict[idx] += "\n" + val

    # Chuyển đổi thành DataFrame
    df = pd.DataFrame(list(data_dict.items()), columns=['Index', 'Data'])

    # Xuất ra file Excel
    writer = pd.ExcelWriter(output_file, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # Định dạng Wrap Text cho cột Data
    worksheet = writer.sheets['Sheet1']
    for row in range(2, len(df) + 2):
        cell = worksheet.cell(row=row, column=2)
        cell.alignment = cell.alignment.copy(wrapText=True)
    
    writer.close()
    print(f"Đã xuất thành công ra file: {output_file} (Giữ nguyên thứ tự)")

# Sử dụng hàm
export_to_excel_ordered('index.txt', 'data.txt', 'ket_qua.xlsx')
