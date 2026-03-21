from playsound import playsound
import os

audio_files = ["audio1.mp3", "audio2.mp3"]

for file in audio_files:
    if os.path.exists(file):
        print(f"Đang phát: {file}")
        playsound(file) # Hàm này sẽ tự đợi phát xong mới chuyển bài tiếp theo
