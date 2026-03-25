import pyautogui
import time

def find_and_click_submit():
    try:
        # Tìm tọa độ tâm của hình ảnh trên màn hình
        # Lưu ý: Cần cài thêm thư viện opencv-python để dùng được tham số confidence (độ chính xác)
        submit_x, submit_y = pyautogui.locateCenterOnScreen('submit_btn.png', confidence=0.8)
        
        # Di chuyển chuột tới đó và click
        pyautogui.click(submit_x, submit_y)
        print("Đã click nút Submit!")
        
    except pyautogui.ImageNotFoundException:
        # Nếu giao diện giãn quá dài làm nút Submit bị khuất khỏi màn hình
        # Bạn có thể kết hợp thêm thao tác cuộn chuột (scroll) xuống trước khi tìm lại
        pyautogui.scroll(-500) 
        time.sleep(1)
        # Gọi lại hàm tìm kiếm hoặc xử lý lỗi ở đây
        print("Không thấy nút, đã cuộn trang xuống...")
