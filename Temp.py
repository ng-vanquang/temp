import multiprocessing
import time

def cpu_stresser():
    # Vòng lặp tính toán vô hạn để vắt kiệt CPU
    while True:
        pass

if __name__ == '__main__':
    # Lấy số lượng CPU core hiện có
    cores = multiprocessing.cpu_count()
    print(f"Bắt đầu tăng tải trên {cores} CPU cores. Nhấn Ctrl+C để dừng.")
    
    processes = []
    
    try:
        # Tạo và khởi chạy các process
        for i in range(cores):
            p = multiprocessing.Process(target=cpu_stresser)
            p.start()
            processes.append(p)
            
        # Giữ cho script chính chạy
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nĐang dừng các tiến trình...")
        for p in processes:
            p.terminate()
            p.join()
        print("Đã hoàn tất dọn dẹp.")
