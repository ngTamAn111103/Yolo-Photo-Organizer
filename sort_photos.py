import os
import shutil
import json
from ultralytics import YOLO
from dotenv import load_dotenv
import time

start_time = time.monotonic()

# --- 1. TẢI CẤU HÌNH TỪ .ENV ---
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lấy các hằng số từ file .env
MODEL_NAME = os.getenv("MODEL_NAME", "yolov8n.pt")
CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
DEVICE = os.getenv("DEVICE", "cpu") # Đã dùng ở predict
SOURCE_DIR_NAME = os.getenv("SOURCE_DIR_NAME", "source")
OUTPUT_DIR_NAME = os.getenv("OUTPUT_DIR_NAME", "result") # Sửa lại cho khớp .env gốc
DB_FILE_NAME = os.getenv("DB_FILE_NAME", "database.json")

# --- CẢI TIẾN: Lấy thêm cấu hình tăng tốc ---
IMG_SIZE = int(os.getenv("IMG_SIZE", 640))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 8))
USE_HALF = os.getenv("USE_HALF_PRECISION", "True").lower() == "true"
NUM_WORKERS = int(os.getenv("NUM_WORKERS", 8))

# Xây dựng các đường dẫn tuyệt đối
SOURCE_DIR = os.path.join(BASE_DIR, SOURCE_DIR_NAME)
OUTPUT_DIR = os.path.join(BASE_DIR, OUTPUT_DIR_NAME)
DB_FILE_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)

SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')

# --- 2. TẢI MÔ HÌNH ---
# print(f"Đang tải mô hình {MODEL_NAME}...")
try:
    model = YOLO(MODEL_NAME)
    class_names = model.names
    # print("Tải mô hình thành công.")
    # print(f"Sử dụng thiết bị: {DEVICE} | Kích thước lô: {BATCH_SIZE}")
except Exception as e:
    print(f"LỖI: Không thể tải mô hình {MODEL_NAME}. Lỗi: {e}")
    exit()

# --- 3. CẢI TIẾN: TÍNH NĂNG "RESUME" (TIẾP TỤC) VỚI LỰA CHỌN ---
database_data = {}
processed_images = set()
resume_processing = False # Biến để quyết định có tải CSDL cũ không

if os.path.exists(DB_FILE_PATH):
    # print(f"Đã tìm thấy file CSDL cũ ({DB_FILE_NAME}).")
    
    # --- THÊM LỰA CHỌN CHO NGƯỜI DÙNG ---
    choice = ""
    while choice not in ['y', 'n']:
        choice = input("Bạn có muốn chạy tiếp (resume) [y] hay chạy mới (xóa cũ) [n]? ").lower().strip()

    if choice == 'y':
        print("Đang tải CSDL cũ để tiếp tục (resume)...")
        resume_processing = True
    else:
        print("OK. Sẽ bắt đầu xử lý mới (CSDL cũ sẽ bị ghi đè khi kết thúc).")
        database_data = {}
        processed_images = set()
    # --- KẾT THÚC LỰA CHỌN ---

else:
    print("Không tìm thấy CSDL cũ. Bắt đầu xử lý mới.")

# Chỉ tải file nếu người dùng chọn 'y'
if resume_processing:
    try:
        with open(DB_FILE_PATH, 'r', encoding='utf-8') as f:
            database_data = json.load(f)
            processed_images = set(database_data.keys())
            print(f"Đã tìm thấy {len(processed_images)} ảnh đã xử lý.")
    except json.JSONDecodeError:
        print(f"LỖI: File {DB_FILE_NAME} bị hỏng. Sẽ bắt đầu lại từ đầu.")
        database_data = {}
        processed_images = set()

# --- 4. CẢI TIẾN: LẤY DANH SÁCH ẢNH VÀ CHIA LÔ (BATCH) ---
# print(f"Bắt đầu quét thư mục: {SOURCE_DIR}")
os.makedirs(OUTPUT_DIR, exist_ok=True)

all_image_paths = []
images_to_process = []

for image_name in os.listdir(SOURCE_DIR):
    if not image_name.lower().endswith(SUPPORTED_EXTENSIONS):
        continue
    
    # Tính năng Resume: Chỉ xử lý ảnh chưa có trong CSDL
    if image_name not in processed_images:
        images_to_process.append(os.path.join(SOURCE_DIR, image_name))
    else:
        all_image_paths.append(os.path.join(SOURCE_DIR, image_name)) # Vẫn thêm vào danh sách tổng

total_new_images = len(images_to_process)
if total_new_images == 0:
    print("Không có ảnh mới nào để xử lý. Đã bỏ qua.")
else:
    print(f"Tìm thấy {total_new_images} ảnh mới cần xử lý (trong tổng số {len(all_image_paths) + total_new_images} ảnh).")

processed_count = 0

# Lặp qua các lô ảnh cần xử lý
for i in range(0, total_new_images, BATCH_SIZE):
    batch_paths = images_to_process[i : i + BATCH_SIZE]
    if not batch_paths:
        continue
        
    print(f"\nĐang xử lý lô {i//BATCH_SIZE + 1}/{(total_new_images + BATCH_SIZE - 1)//BATCH_SIZE} (ảnh {i+1} đến {min(i + BATCH_SIZE, total_new_images)})...")

    try:
        # ----- CHẠY SUY LUẬN (THEO LÔ) -----
        # Sử dụng biến DEVICE từ .env, không hardcode 'mps'
        results = model.predict(
            batch_paths, 
            device=DEVICE, 
            verbose=False,
            imgsz=IMG_SIZE,       
            half=USE_HALF,        
            workers=NUM_WORKERS   
        )

        # `results` là một danh sách, lặp qua nó
        for result_index, result in enumerate(results):
            
            image_path = batch_paths[result_index] # Lấy đường dẫn ảnh gốc
            image_name = os.path.basename(image_path)
            
            all_detections_for_db = []
            filtered_classes_for_sorting = set()

            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = class_names[class_id]
                coords = box.xyxy[0].cpu().numpy().astype(int).tolist()

                # 1. LƯU VÀO CSDL (Lưu tất cả)
                all_detections_for_db.append({
                    "class": class_name,
                    "confidence": round(confidence, 2),
                    "box": coords
                })

                # 2. LỌC ĐỂ SẮP XẾP (Chỉ lưu nếu > ngưỡng)
                if confidence >= CONFIDENCE_THRESHOLD:
                    filtered_classes_for_sorting.add(class_name)

            # ----- SAU KHI XỬ LÝ XONG 1 ẢNH (TRONG LÔ) -----
            if all_detections_for_db:
                database_data[image_name] = all_detections_for_db

            if not filtered_classes_for_sorting:
                 print(f"  [Xử lý: {image_name}] - Không tìm thấy vật thể > {CONFIDENCE_THRESHOLD*100}%.")
            else:
                 print(f"  [Xử lý: {image_name}] - Tìm thấy: {list(filtered_classes_for_sorting)}")
                 for class_name in filtered_classes_for_sorting:
                    target_album_dir = os.path.join(OUTPUT_DIR, class_name)
                    os.makedirs(target_album_dir, exist_ok=True)
                    
                    target_file_path = os.path.join(target_album_dir, image_name)
                    shutil.copy2(image_path, target_file_path)
            
            processed_count += 1

    except Exception as e:
        print(f"LỖI khi xử lý lô ảnh bắt đầu từ {batch_paths[0]}: {e}")

# --- 5. HOÀN TẤT VÀ LƯU CSDL ---
print("\nHoàn tất xử lý.")
print(f"Tổng cộng đã xử lý mới: {processed_count} ảnh.")

try:
    with open(DB_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(database_data, f, indent=2, ensure_ascii=False)
    print(f"Đã lưu cơ sở dữ liệu vào: {DB_FILE_PATH}")
except Exception as e:
    print(f"LỖI khi ghi file JSON: {e}")

end_time = time.monotonic()
total_duration = end_time - start_time
print(f"Tổng thời gian chạy: {total_duration:.2f} giây.")