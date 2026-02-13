import os
import wave
import contextlib

def validate_wav_file(file_path):
    """
    Kiểm tra file .wav với các tiêu chí:
    1. Tồn tại
    2. Định dạng .wav
    3. Dung lượng > 0 bytes
    4. Không bị lỗi header/corrupt
    5. Thời lượng > 0 giây
    
    Returns:
        (bool, str): (True/False, Thông báo chi tiết)
    """
    
    # Rule 1: Kiểm tra file tồn tại
    if not os.path.exists(file_path):
        return False, "Lỗi: File không tồn tại."

    # Rule phụ: Kiểm tra đuôi file
    if not file_path.lower().endswith('.wav'):
        return False, "Lỗi: File không phải định dạng .wav."

    # Rule phụ: Kiểm tra dung lượng file (tránh file rỗng 0 bytes)
    if os.path.getsize(file_path) == 0:
        return False, "Lỗi: File có dung lượng 0 bytes."

    try:
        # Sử dụng contextlib để đảm bảo file được đóng sau khi mở
        with contextlib.closing(wave.open(file_path, 'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            
            # Tính thời lượng
            duration = frames / float(rate)
            
            # Rule 3: Kiểm tra thời lượng
            if duration <= 0:
                return False, "Lỗi: File có thời lượng 0 giây."
                
            # (Optional) Bạn có thể in ra thông tin file nếu cần
            # print(f"File OK: {duration:.2f}s, {rate}Hz, {f.getnchannels()} channels")
            
            return True, f"Hợp lệ (Duration: {duration:.2f}s)"

    # Rule 2: Kiểm tra file lỗi (Corrupted)
    except wave.Error as e:
        return False, f"Lỗi: File audio bị hỏng hoặc sai định dạng header ({e})."
    except EOFError:
        return False, "Lỗi: File audio bị cắt cụt (EOF Error)."
    except Exception as e:
        return False, f"Lỗi không xác định: {e}"

# --- Ví dụ sử dụng ---
if __name__ == "__main__":
    # Test các trường hợp
    files_to_test = [
        "audio_chuan.wav", 
        "khong_ton_tai.wav", 
        "file_loi.wav"
    ]

    # Tạo file giả để test (bạn cần thay bằng đường dẫn file thật của bạn)
    # Open file test thật của bạn ở đây
    
    print(f"{'KẾT QUẢ KIỂM TRA':<20} | {'MESSAGE'}")
    print("-" * 50)
    
    path = "sample.wav" # Thay đường dẫn file của bạn vào đây
    is_valid, message = validate_wav_file(path)
    print(f"{str(is_valid):<20} | {message}")
