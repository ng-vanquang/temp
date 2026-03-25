import pyautogui
import time

def find_and_click_submit():
    max_scrolls = 5
    scroll_amount = -500  # Thông số cuộn xuống (số âm là cuộn xuống, bạn có thể tăng giảm tùy độ dài web)
    
    for attempt in range(max_scrolls):
        try:
            # Cố gắng tìm nút submit trên màn hình hiện tại
            # Yêu cầu đã cài: pip install opencv-python
            submit_pos = pyautogui.locateCenterOnScreen('submit_btn.png', confidence=0.8)
            
            if submit_pos:
                # Nếu tìm thấy, di chuyển chuột và click
                pyautogui.click(submit_pos.x, submit_pos.y)
                print(f"Đã tìm thấy và click nút Submit ở lần thử thứ {attempt + 1}!")
                return True  # Bấm xong thì thoát hàm để làm việc khác
                
        except pyautogui.ImageNotFoundException:
            # Nếu không tìm thấy ảnh, exception sẽ bật ra và chạy vào đây
            print(f"Lần {attempt + 1}: Chưa thấy nút Submit, đang cuộn trang xuống...")
            pyautogui.scroll(scroll_amount)
            
            # Bắt buộc phải có thời gian nghỉ ngắn để trình duyệt render xong thao tác cuộn
            time.sleep(1) 
    
    # Nếu chạy hết vòng lặp (5 lần) mà vẫn không thấy
    print("Cảnh báo: Đã cuộn 5 lần nhưng vẫn không tìm thấy nút Submit. Vui lòng kiểm tra lại ảnh mẫu!")
    return False

# Gọi thử hàm
# find_and_click_submit()
