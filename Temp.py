import multiprocessing
import time
import sys

def cpu_worker(target_percent):
    """
    Tạo tải cho 1 core ở một mức phần trăm nhất định bằng phương pháp Duty Cycle.
    """
    # Nếu set 0%, không làm gì cả
    if target_percent <= 0:
        while True:
            time.sleep(1)
            
    # Nếu set 100%, chạy vòng lặp vô hạn vắt kiệt core
    if target_percent >= 100:
        while True:
            pass

    # Phân bổ thời gian hoạt động và nghỉ ngơi
    work_time = target_percent / 100.0
    sleep_time = 1.0 - work_time
    cycle_time = 0.1  # Chu kỳ 100ms (0.1 giây) để biểu đồ mượt mà
    
    actual_work = work_time * cycle_time
    actual_sleep = sleep_time * cycle_time

    while True:
        start = time.time()
        # Trạng thái Active: Bắt CPU tính toán
        while time.time() - start < actual_work:
            pass
        # Trạng thái Idle: Cho CPU nghỉ ngơi
        time.sleep(actual_sleep)

def main():
    # ==========================================
    # ⚙️ BẠN CÓ THỂ TÙY CHỈNH THÔNG SỐ Ở ĐÂY ⚙️
    # ==========================================
    TARGET_CPU_PERCENT = 60  # Mức % CPU muốn sử dụng (trên mỗi core)
    
    TOTAL_RAM_GB = 110       # Tổng số RAM vật lý của server (GB)
    TARGET_RAM_PERCENT = 60  # Mức % RAM muốn chiếm dụng
    # ==========================================

    print("=" * 50)
    print("🚀 BẮT ĐẦU CÔNG CỤ TẠO TẢI CPU & RAM 🚀")
    print("=" * 50)

    # 1. KHỞI CHẠY TIẾN TRÌNH ÉP TẢI CPU
    cores = multiprocessing.cpu_count()
    print(f"\n[CPU] Đang khởi chạy mức tải ~{TARGET_CPU_PERCENT}% trên toàn bộ {cores} cores...")
    
    cpu_processes = []
    for _ in range(cores):
        p = multiprocessing.Process(target=cpu_worker, args=(TARGET_CPU_PERCENT,))
        p.start()
        cpu_processes.append(p)
    
    # 2. KHỞI CHẠY TIẾN TRÌNH ÉP TẢI RAM
    print(f"\n[RAM] Máy chủ khai báo: {TOTAL_RAM_GB} GB RAM.")
    
    gb_to_bytes = 1024 * 1024 * 1024
    target_bytes = int((TOTAL_RAM_GB * (TARGET_RAM_PERCENT / 100.0)) * gb_to_bytes)
    target_gb_display = target_bytes / gb_to_bytes
    
    print(f"[RAM] Mục tiêu chiếm dụng: {TARGET_RAM_PERCENT}% (Khoảng {target_gb_display:.2f} GB)")
    
    dummy_memory = []
    bytes_allocated = 0
    chunk_size = gb_to_bytes  # Cấp phát 1GB mỗi lần

    try:
        while bytes_allocated < target_bytes:
            # Điều chỉnh lượng cấp phát cuối cùng cho khớp chính xác
            if target_bytes - bytes_allocated < chunk_size:
                chunk_size = target_bytes - bytes_allocated
            
            # Ghi trực tiếp chuỗi byte vào RAM
            dummy_memory.append(b'x' * chunk_size)
            bytes_allocated += chunk_size
            
            print(f"[RAM] Đang cấp phát... Đã chiếm dụng: {bytes_allocated / gb_to_bytes:.2f} GB")
            time.sleep(0.5)  # Tránh làm hệ điều hành bị "ngộp"
            
        print("\n✅ ĐÃ ĐẠT MỤC TIÊU TẢI CHO CẢ CPU VÀ RAM!")
        print("⏳ Đang duy trì trạng thái... (Nhấn Ctrl+C để dừng và giải phóng tài nguyên)")
        
        # Giữ cho script chính sống để duy trì RAM và quản lý tiến trình con
        while True:
            time.sleep(1)

    except MemoryError:
        print("\n❌ [Lỗi] Tràn bộ nhớ! Hệ điều hành từ chối cấp phát thêm RAM (OOM).")
    except KeyboardInterrupt:
        print("\n\n🛑 Đã nhận lệnh dừng (Ctrl+C). Đang tiến hành dọn dẹp hệ thống...")
    finally:
        # 3. DỌN DẸP TÀI NGUYÊN AN TOÀN KHI THOÁT
        print("[Dọn dẹp] Đang tắt các tiến trình CPU...")
        for p in cpu_processes:
            p.terminate()
            p.join()
            
        print("[Dọn dẹp] Đang giải phóng bộ nhớ RAM ảo...")
        del dummy_memory
        
        print("✨ Hoàn tất! Hệ thống đã được trả lại trạng thái bình thường.")
        sys.exit(0)

if __name__ == '__main__':
    main()
