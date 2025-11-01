import os
import shutil
import json
from ultralytics import YOLO
from dotenv import load_dotenv # <--- Thêm vào
import time
start_time = time.monotonic() # <--- THÊM VÀO (2/4): Lấy thời gian bắt đầu
# --- 1. TẢI CẤU HÌNH TỪ .ENV ---
load_dotenv() # <--- Thêm vào

# Lấy đường dẫn cơ sở của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lấy các hằng số từ file .env
MODEL_NAME = os.getenv("MODEL_NAME", "yolov8n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
DEVICE = os.getenv("DEVICE", "mps")
SOURCE_DIR_NAME = os.getenv("SOURCE_DIR_NAME", "source")
OUTPUT_DIR_NAME = os.getenv("OUTPUT_DIR_NAME", "images_da_sap_xep")
DB_FILE_NAME = os.getenv("DB_FILE_NAME", "database.json")

# Xây dựng các đường dẫn tuyệt đối
SOURCE_DIR = os.path.join(BASE_DIR, SOURCE_DIR_NAME)
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT_DIR_NAME)
DB_FILE_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# --- 2. TẢI MÔ HÌNH ---
print(f"Đang tải mô hình {MODEL_NAME}...")
# Tải mô hình. Lần chạy đầu tiên có thể mất một chút để tải file .pt
model = YOLO(MODEL_NAME)

# Lấy danh sách tên của các lớp (ví dụ: 'person', 'car', 'dog')
class_names = model.names
print("Tải mô hình thành công.")

# --- 3. KHỞI TẠO CSDL VÀ XỬ LÝ ---
database_data = {} # Cấu trúc JSON chính
processed_count = 0

print(f"Bắt đầu quét thư mục: {SOURCE_DIR}")

# Đảm bảo thư mục đầu ra tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Lặp qua tất cả các file trong thư mục nguồn
for image_name in os.listdir(SOURCE_DIR):
    # Kiểm tra xem file có phải là ảnh không
    if not image_name.lower().endswith(SUPPORTED_EXTENSIONS):
        continue

    image_path = os.path.join(SOURCE_DIR, image_name)
    
    # Danh sách để lưu trữ TẤT CẢ các phát hiện cho CSDL
    all_detections_for_db = []
    
    # Sử dụng SET để lưu các lớp đã lọc (tránh trùng lặp album)
    filtered_classes_for_sorting = set()

    try:
        # ----- CHẠY SUY LUẬN -----
        # device='mps' sẽ sử dụng GPU/Neural Engine của M4
        # verbose=False để tắt bớt log rườm rà
        results = model.predict(image_path, device='mps', verbose=False)

        # `results` là một danh sách, nhưng vì ta chỉ xử lý 1 ảnh, ta lấy phần tử đầu
        result = results[0]

        # Lặp qua từng vật thể được phát hiện trong ảnh
        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = class_names[class_id] # Lấy tên lớp từ ID

            # ***** NÂNG CẤP QUAN TRỌNG *****
            # Lấy tọa độ (x1, y1, x2, y2)
            # Chuyển sang numpy, sang kiểu int, rồi sang list Python
            coords = box.xyxy[0].cpu().numpy().astype(int).tolist()

            # 1. LƯU VÀO CSDL (Lưu tất cả)
            all_detections_for_db.append({
                "class": class_name,
                "confidence": round(confidence, 2), # Làm tròn cho dễ đọc
                "box": coords
            })

            # 2. LỌC ĐỂ SẮP XẾP (Chỉ lưu nếu > ngưỡng)
            if confidence >= CONFIDENCE_THRESHOLD:
                filtered_classes_for_sorting.add(class_name)

        # ----- SAU KHI XỬ LÝ XONG 1 ẢNH -----
        
        # Cập nhật CSDL trong bộ nhớ
        if all_detections_for_db:
            database_data[image_name] = all_detections_for_db

        # Sắp xếp file vào album
        if not filtered_classes_for_sorting:
            print(f"  [Xử lý: {image_name}] - Không tìm thấy vật thể > {CONFIDENCE_THRESHOLD*100}%.")
        else:
            print(f"  [Xử lý: {image_name}] - Tìm thấy: {list(filtered_classes_for_sorting)}")
            # Lặp qua các album cần sao chép ảnh vào
            for class_name in filtered_classes_for_sorting:
                # Tạo thư mục album nếu chưa có (ví dụ: /images_da_sap_xep/person/)
                target_album_dir = os.path.join(OUTPUT_DIR, class_name)
                os.makedirs(target_album_dir, exist_ok=True)
                
                # Sao chép file
                target_file_path = os.path.join(target_album_dir, image_name)
                shutil.copy2(image_path, target_file_path)
        
        processed_count += 1

    except Exception as e:
        print(f"LỖI khi xử lý ảnh {image_name}: {e}")

# --- 4. HOÀN TẤT VÀ LƯU CSDL ---
print("\nHoàn tất xử lý.")
print(f"Tổng cộng đã xử lý: {processed_count} ảnh.")

# Ghi file JSON
try:
    with open(DB_FILE_PATH, 'w', encoding='utf-8') as f:
        # indent=2 để file JSON đẹp, dễ đọc
        # ensure_ascii=False để hỗ trợ ký tự (nếu có)
        json.dump(database_data, f, indent=2, ensure_ascii=False)
    print(f"Đã lưu cơ sở dữ liệu vào: {DB_FILE_PATH}")
except Exception as e:
    print(f"LỖI khi ghi file JSON: {e}")

# Lấy thời gian kết thúc và tính toán
end_time = time.monotonic() # <--- THÊM VÀO (3/4): Lấy thời gian kết thúc
total_duration = end_time - start_time # <--- THÊM VÀO (4/4): Tính toán
print(f"Tổng thời gian chạy: {total_duration:.2f} giây.") # In kết quả