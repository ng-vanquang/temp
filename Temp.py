from playwright.sync_api import sync_playwright
import time
import os

# Thư mục chứa các file target
folder_path = "path/to/your/langpack_folder"

# Cấu hình mapping giữa tên file và direction
lang_mapping = {
    "en.txt": "vien",
    "it.txt": "viit",
    "ar.txt": "viar",
    # Thêm các ngôn ngữ khác vào đây...
}

def automate_testset_grading():
    with sync_playwright() as p:
        # Mở trình duyệt (để headless=False để bạn nhìn thấy thao tác)
        browser = p.chromium.launch(headless=False) 
        page = browser.new_page()
        
        # Truy cập trang web chấm điểm (cần đăng nhập nếu có)
        page.goto("URL_TRANG_WEB_CUA_BAN")

        # Quét các file trong thư mục
        for filename in os.listdir(folder_path):
            if filename in lang_mapping:
                direction_code = lang_mapping[filename]
                file_path = os.path.join(folder_path, filename)

                # 1. Điền direction (Cần thay thế selector tương ứng)
                page.fill("input#direction_input_id", direction_code)

                # 2. Upload file target
                page.set_input_files("input[type='file']", file_path)

                # 3. Đợi 2 giây theo đúng quy trình
                time.sleep(2)

                # 4. Bấm submit
                page.click("button#submit_button_id")

                # (Tùy chọn) Đợi trang phản hồi/tải xong kết quả rồi mới chạy file tiếp theo
                page.wait_for_load_state("networkidle")
                
                print(f"Đã submit thành công file: {filename}")

        browser.close()

if __name__ == "__main__":
    automate_testset_grading()
