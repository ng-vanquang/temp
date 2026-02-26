import multiprocessing
import time

def partial_load(target_percentage):
    """
    Tạo tải cho 1 core ở một mức phần trăm nhất định.
    """
    work_time = target_percentage / 100.0
    sleep_time = 1.0 - work_time
    
    # Chia nhỏ chu kỳ thành 0.1 giây để phân bổ tải mượt mà hơn trên biểu đồ OS
    cycle_time = 0.1
    actual_work = work_time * cycle_time
    actual_sleep = sleep_time * cycle_time

    while True:
        start = time.time()
        # Tính toán liên tục để vắt sức CPU (Active)
        while time.time() - start < actual_work:
            pass
        # Cho CPU nghỉ ngơi để hạ nhiệt độ và giảm % sử dụng (Idle)
        time.sleep(actual_sleep)

if __name__ == '__main__':
    cores = multiprocessing.cpu_count()
    target_usage = 60  # Đặt mức % CPU bạn muốn giữ
    
    print(f"Bắt đầu tạo tải khoảng {target_usage}% trên toàn bộ {cores} CPU cores...")
    print("Nhấn Ctrl+C để dừng.")
    
    processes = []
    try:
        # Chạy tác vụ trên tất cả các core
        for _ in range(cores):
            p = multiprocessing.Process(target=partial_load, args=(target_usage,))
            p.start()
            processes.append(p)
            
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nĐang dừng các tiến trình...")
        for p in processes:
            p.terminate()
            p.join()
        print("Đã hoàn tất dọn dẹp.")
