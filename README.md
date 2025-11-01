# Dự án Phân loại Ảnh bằng YOLO

Đây là một công cụ Python giúp tự động quét, phân loại, và tổ chức một album ảnh. Nó sử dụng mô hình AI (YOLO) để phát hiện các đối tượng trong ảnh và xây dựng một cơ sở dữ liệu JSON. Sau đó, một giao diện đồ họa (GUI) cho phép người dùng duyệt ảnh theo các "tag" (nhãn) đã được AI phát hiện.

## 🚀 Tính năng

  * **Phát hiện đối tượng:** Tự động phát hiện 80+ loại đối tượng (người, xe cộ, động vật, đồ vật...) bằng mô hình YOLO.
  * **Lưu trữ thông minh:** Lưu tất cả kết quả (gồm tên lớp, độ tin cậy, và tọa độ) vào một file `database.json`.
  * **Tự động sắp xếp:** Tự động sao chép ảnh vào các thư mục (`result/`) dựa trên các vật thể được tìm thấy.
  * **Giao diện trực quan:** Một trình xem ảnh (GUI) full-screen cho phép duyệt ảnh theo Tag.
  * **Hỗ trợ Tiếng Việt:** Các tag được tự động dịch sang Tiếng Việt trên giao diện.
  * **Dễ cấu hình:** Quản lý toàn bộ cấu hình (như dùng CPU/GPU, tên mô hình) qua một file `.env` duy nhất.

## 📁 Cấu trúc Thư mục

```
/YoloV11_AnNguyen/
├── .venv/                   # Thư mục môi trường ảo (sau khi cài đặt)
├── source/                  # <-- ĐỂ ẢNH GỐC CỦA BẠN VÀO ĐÂY
├── result/                  # (Tự động tạo) Chứa các album ảnh đã sắp xếp
│   ├── person/
│   ├── car/
│   └── ...
├── .env                     # File cấu hình (bạn phải tự tạo)
├── .gitignore               # (Nên có) Để bỏ qua các file .pt, .venv
├── requirements.txt         # File chứa các thư viện cần thiết
├── sort_photos.py           # Script 1: Chạy AI để phân tích và sắp xếp
├── view_database.py         # Script 2: Chạy GUI để xem kết quả
└── database.json            # (Tự động tạo) Cơ sở dữ liệu chứa kết quả AI
```

-----

## 🛠️ Cài đặt

### Bước 1: Tạo file `requirements.txt`

Tạo một file tên là `requirements.txt` trong thư mục gốc của dự án và dán nội dung sau vào:

```txt
ultralytics
python-dotenv
customtkinter
Pillow
```

### Bước 2: Tạo file `.env`

Tạo một file tên là `.env` và dán nội dung sau vào. Đây là nơi bạn cấu hình dự án.

```ini
# === CẤU HÌNH SCRIPT SẮP XẾP (sort_photos.py) ===

# Tên mô hình YOLO (ví dụ: yolov8n.pt, yolov8m.pt, yolo11m.pt)
MODEL_NAME="yolo11m.pt"

# Ngưỡng tin cậy (ví dụ: 0.5 cho 50%)
CONFIDENCE_THRESHOLD=0.5

# Thiết bị chạy AI: 'mps' (GPU Mac), 'cpu' (CPU)
DEVICE="mps"


# === CẤU HÌNH TÊN THƯ MỤC VÀ FILE ===

# Tên thư mục chứa ảnh gốc
SOURCE_DIR_NAME="source"

# Tên thư mục chứa ảnh đã sắp xếp
OUTPUT_DIR_NAME="result"

# Tên file cơ sở dữ liệu JSON
DB_FILE_NAME="database.json"
```

### Bước 3: Cài đặt Môi trường ảo (`.venv`) và Thư viện

Mở Terminal và trỏ đến thư mục dự án của bạn.

1.  **Tạo môi trường ảo:**

    ```bash
    python3 -m venv .venv
    ```

2.  **Kích hoạt môi trường ảo:**

      * Trên macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
      * Trên Windows:
        ```bash
        .venv\Scripts\activate
        ```
      * (Bạn sẽ thấy tên `(.venv)` xuất hiện ở đầu dòng lệnh).

3.  **Cài đặt các thư viện:**

    ```bash
    pip install -r requirements.txt
    ```

-----

## 🏃 Cách sử dụng

### Bước 1: Chuẩn bị Ảnh

  * **Sao chép tất cả ảnh gốc** của bạn (chỉ `.jpg`, `.jpeg`, `.png`) vào thư mục `source/`.
  * **Kiểm tra file `.env`** để chắc chắn các cấu hình (đặc biệt là `DEVICE`) đã đúng ý bạn.

### Bước 2: Chạy Script Phân loại (AI)

Đây là bước bắt buộc để tạo CSDL. Đảm bảo môi trường `(.venv)` đã được kích hoạt.

```bash
python3 sort_photos.py
```

  * **Script này làm gì?** Nó sẽ quét thư mục `source/`, dùng mô hình AI (YOLO) để phân tích từng ảnh.
  * **Kết quả:**
    1.  File `database.json` được tạo ra, chứa tọa độ và tên của mọi vật thể.
    2.  Thư mục `result/` được tạo ra, chứa các thư mục con (ví dụ: `person`, `car`) là các bản sao của ảnh gốc.
  * Quá trình này có thể mất vài phút tùy vào số lượng ảnh và sức mạnh máy của bạn (chạy `mps` sẽ nhanh hơn `cpu`).

### Bước 3: Chạy Trình xem ảnh (GUI)

Sau khi `database.json` đã được tạo, bạn có thể chạy trình xem.

```bash
python3 view_database.py
```

  * **Script này làm gì?** Nó sẽ đọc file `database.json` và các ảnh trong `source/`.
  * **Kết quả:** Một cửa sổ full-screen sẽ hiện ra.
      * **Thanh trên cùng:** Các Tag (như "Người (person)", "Xe hơi (car)") để bạn chọn.
      * **Cột bên trái:** Danh sách các file ảnh thuộc Tag bạn vừa chọn.
      * **Khung chính bên phải:** Hiển thị ảnh (đã vẽ các hộp phát hiện) khi bạn bấm vào một tên ảnh.

-----

## 📜 Chức năng các File `.py`

### `sort_photos.py` (Script Phân tích AI)

  * **Mục đích:** Xử lý hàng loạt và tạo ra cơ sở dữ liệu.
  * **Logic hoạt động:**
    1.  Đọc các cấu hình từ file `.env` (tên mô hình, ngưỡng, thiết bị, tên thư mục).
    2.  Tải mô hình YOLO (`MODEL_NAME`) về máy.
    3.  Lặp qua từng file ảnh trong thư mục `source/`.
    4.  Cho từng ảnh, chạy `model.predict()` (sử dụng `DEVICE` là `mps` hoặc `cpu`).
    5.  Thu thập **tất cả** kết quả (lớp, độ tin cậy, tọa độ `box`) và lưu vào một cấu trúc dữ liệu.
    6.  Lọc ra các kết quả có độ tin cậy cao hơn `CONFIDENCE_THRESHOLD` để sao chép ảnh vào các thư mục `result/`.
    7.  Sau khi lặp xong, ghi toàn bộ cấu trúc dữ liệu thu thập được vào file `database.json`.
    8.  In ra tổng thời gian xử lý.

### `view_database.py` (Script Trình xem GUI)

  * **Mục đích:** Cung cấp giao diện đồ họa để người dùng xem và duyệt kết quả của AI.
  * **Logic hoạt động:**
    1.  Đọc các đường dẫn từ file `.env` (để biết tìm `database.json` và `source/` ở đâu).
    2.  Tải toàn bộ file `database.json` vào bộ nhớ.
    3.  Tạo một cửa sổ full-screen bằng CustomTkinter.
    4.  Xử lý dữ liệu: Xây dựng một "bản đồ" từ các Tag (ví dụ: "person") đến danh sách các ảnh chứa tag đó (ví dụ: `['img1.jpg', 'img5.jpg']`).
    5.  Hiển thị tất cả các "key" (Tag) của bản đồ đó lên thanh cuộn ngang trên cùng, tra cứu từ điển `TRANSLATION_DICT` để hiển thị Tiếng Việt.
    6.  **Khi bấm vào một Tag:**
          * Làm sạch Cột 2 (danh sách ảnh).
          * Lấy danh sách ảnh cho Tag đó và tạo các nút bấm (button) ở Cột 2.
    7.  **Khi bấm vào một ảnh (Cột 2):**
          * Tìm ảnh gốc trong thư mục `source/`.
          * Lấy dữ liệu phát hiện (tọa độ, tên lớp) của ảnh đó từ `database.json`.
          * Dùng thư viện Pillow (PIL) để vẽ các hình chữ nhật và văn bản lên ảnh.
          * Tính toán tỷ lệ (aspect ratio) để hiển thị ảnh vừa vặn trong Khung 3 mà không bị méo.
          * Hiển thị ảnh đã vẽ lên giao diện.