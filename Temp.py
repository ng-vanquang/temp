import pygame
import os
import time

def play_playlist(audio_files):
    # Khởi tạo mixer của pygame
    pygame.mixer.init()
    
    current_index = 0
    total_files = len(audio_files)

    print(f"--- Bắt đầu phát danh sách ({total_files} file) ---")

    while current_index < total_files:
        file_path = audio_files[current_index]
        
        # Kiểm tra file tồn tại
        if not os.path.exists(file_path):
            print(f"[Lỗi] Không tìm thấy: {file_path}")
            current_index += 1
            continue

        print(f"\n[Đang phát] {os.path.basename(file_path)}")
        
        try:
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()

            # Vòng lặp chờ file hiện tại phát xong
            while pygame.mixer.music.get_busy():
                # Nghỉ một khoảng ngắn để tránh tốn tài nguyên CPU
                time.sleep(0.1) 
                
            print(f"[Hoàn thành] {os.path.basename(file_path)}")
            current_index += 1

        except Exception as e:
            print(f"[Lỗi khi phát file] {e}")
            current_index += 1

    print("\n--- Đã phát hết danh sách ---")
    pygame.mixer.quit()

if __name__ == "__main__":
    # Thay thế list này bằng đường dẫn thực tế của bạn
    # Bạn có thể dùng os.listdir() để lấy toàn bộ file trong 1 folder
    my_playlist = [
        "audio1.mp3",
        "audio2.wav",
        "path/to/your/audio3.mp3"
    ]

    if my_playlist:
        play_playlist(my_playlist)
    else:
        print("Danh sách phát trống.")
