Chắc chắn rồi, đây là file `README.md` hoàn chỉnh được tổng hợp từ tất cả các file và thông tin bạn đã cung cấp.
`README này do AI tạo💁🏽, nếu có gì thắc mắc vui lòng liên hệ telegram:`
```bash
@annguyen3528
```
`Nếu thấy dự án nhỏ này hữu ích, hãy mời tôi 1 ly cà phê:`
```bash
VPBank
3528111103
NGUYEN TAM AN
```
-----

# Dự án Sắp xếp và Duyệt ảnh bằng YOLO

Đây là một bộ công cụ Python mạnh mẽ sử dụng AI (YOLO) để tự động quét, phân tích và sắp xếp một thư viện ảnh lớn. Dự án bao gồm hai phần chính: một script "backend" (`sort_photos.py`) để xử lý ảnh hàng loạt và một giao diện đồ họa "frontend" (`view_database.py`) để duyệt kết quả một cách trực quan.

## 🚀 Tính năng

  * **Phân tích AI hàng loạt:** Sử dụng các mô hình YOLO (bao gồm YOLOv11, YOLOv12) để quét hàng nghìn ảnh và phát hiện 80+ loại đối tượng.
  * **Cơ sở dữ liệu JSON:** Lưu trữ tất cả các vật thể tìm thấy (với độ tin cậy \> ngưỡng) vào một file `db.json` duy nhất để dễ dàng truy vấn.
  * **Tự động sắp xếp:** Tự động *sao chép* ảnh vào các thư mục con (`result/person`, `result/car`...) dựa trên các vật thể được phát hiện.
  * **Tính năng "Resume" thông minh:** Khi chạy lại, script sẽ hỏi bạn muốn chạy tiếp hay chạy mới, tự động bỏ qua các ảnh đã xử lý để tiết kiệm thời gian.
  * **Tối ưu hiệu suất:** Cấu hình đầy đủ các tham số tăng tốc (`BATCH_SIZE`, `IMG_SIZE`, `USE_HALF_PRECISION`, `NUM_WORKERS`) để tận dụng tối đa GPU (NVIDIA Cuda hoặc Apple MPS).
  * **Trình duyệt ảnh GUI:** Giao diện `CustomTkinter` full-screen, cho phép bạn duyệt ảnh theo các "Tag" mà AI tìm thấy.
  * **Hỗ trợ Tiếng Việt:** Toàn bộ Tag và nhãn trên ảnh được tự động dịch sang Tiếng Việt (ví dụ: "Người (person)").
  * **Lọc hiển thị động:** Khi bạn chọn tag "Người", trình xem ảnh sẽ *chỉ vẽ* các hộp xung quanh "Người", ẩn đi các vật thể khác trong ảnh.

-----

## 📁 Cấu trúc Thư mục

Đây là cấu trúc thư mục được đề xuất. Các file/thư mục trong `.gitignore` (như `source/`, `result/`) bạn sẽ cần tự tạo.

```
/Yolo-Photo-Organizer/
├── .venv/                   # (Tự động tạo) Môi trường ảo Python
├── source/                  # <-- ĐỂ ẢNH GỐC CỦA BẠN VÀO ĐÂY (Tự tạo)
├── result/                  # (Tự động tạo) Chứa các album ảnh đã sắp xếp
│   ├── person/
│   ├── car/
│   └── ...
├── .env                     # (BẮT BUỘC) File cấu hình của bạn (Xem bên dưới)
├── .gitignore               # Chứa danh sách các file/thư mục bỏ qua
├── requirements.txt         # Danh sách các thư viện cần thiết
├── sort_photos.py           # Script 1: Chạy AI để phân tích và sắp xếp
├── view_database.py         # Script 2: Chạy GUI để xem kết quả
└── db.json                  # (Tự động tạo) Cơ sở dữ liệu chứa kết quả AI
```

-----

## 🛠️ Cài đặt

### Bước 1: Lấy mã nguồn

Mở Terminal (hoặc Command Prompt) và `git clone` dự án này:

```bash
git clone https://github.com/ngTamAn111103/Yolo-Photo-Organizer.git
cd Yolo-Photo-Organizer
```

### Bước 2: Tạo và Kích hoạt Môi trường ảo

Việc này giúp cô lập các thư viện của dự án.

```bash
# Tạo môi trường ảo
python3 -m venv .venv

# Kích hoạt môi trường (macOS/Linux)
source .venv/bin/activate

# (Hoặc kích hoạt trên Windows)
.venv\Scripts\activate
```

### Bước 3: Cài đặt Thư viện

Cài đặt tất cả các thư viện cần thiết từ file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Bước 4: Tạo Thư mục và File Cấu hình

1.  **Tạo thư mục `source`:** Đây là nơi bạn sẽ đưa ảnh gốc vào.

    ```bash
    mkdir source
    ```

2.  **Tạo file `.env`:** Tạo một file tên `.env` ở thư mục gốc và sao chép toàn bộ nội dung dưới đây vào. *Đây là bước quan trọng nhất.*

    ```ini
    # === CẤU HÌNH SCRIPT SẮP XẾP (sort_photos.py) ===

    # Tên mô hình YOLO (ví dụ: yolov8n.pt, yolo11m.pt, yolo11x.pt)
    MODEL_NAME="yolo11x.pt"

    # Ngưỡng tin cậy (ví dụ: 0.5 cho 50%)
    # Chỉ vật thể > ngưỡng này mới được lưu vào CSDL và sắp xếp
    CONFIDENCE_THRESHOLD=0.5

    # Thiết bị chạy AI: 'mps' (GPU Mac), 'cuda' (NVIDIA GPU), 'cpu' (CPU)
    DEVICE="mps"


    # === CẤU HÌNH TÊN THƯ MỤC VÀ FILE ===

    # Tên thư mục chứa ảnh gốc
    SOURCE_DIR_NAME="source"

    # Tên thư mục chứa ảnh đã sắp xếp
    OUTPUT_DIR_NAME="result"

    # Tên file cơ sở dữ liệu JSON
    DB_FILE_NAME="db.json"

    # === CẤU HÌNH TĂNG TỐC ĐỘ XỬ LÝ ===

    # Số lượng ảnh xử lý cùng lúc. Tăng nếu bạn có nhiều VRAM (GPU).
    BATCH_SIZE=32

    # Kích thước ảnh AI xử lý. 640 là nhanh, 1280 chính xác hơn (chậm hơn).
    IMG_SIZE=640

    # Dùng độ chính xác 16-bit (FP16). Nhanh hơn, tiết kiệm VRAM.
    USE_HALF_PRECISION=True

    # Số luồng CPU chuẩn bị dữ liệu. Tùy thuộc vào số lõi CPU của bạn.
    NUM_WORKERS=8
    ```

-----

## 🏃 Cách sử dụng

### Bước 1: Thêm ảnh

Sao chép tất cả các ảnh (`.jpg`, `.jpeg`, `.png`) bạn muốn phân tích vào thư mục `source/`.

### Bước 2: Chạy Script Phân tích (Script 1)

Đảm bảo môi trường `(.venv)` đã được kích hoạt. Chạy script `sort_photos.py`:

```bash
python3 sort_photos.py
```

  * **Script này làm gì?** Nó sẽ bắt đầu quét thư mục `source/`.
  * **Tính năng Resume:** Nếu nó tìm thấy file `db.json` cũ, nó sẽ hỏi bạn: `Bạn có muốn chạy tiếp (resume) [y] hay chạy mới (xóa cũ) [n]?`.
      * Chọn `y` (yes) để chỉ quét các ảnh mới.
      * Chọn `n` (no) để xóa CSDL cũ và quét lại từ đầu.
  * **Kết quả:**
    1.  File `db.json` được tạo/cập nhật, chứa mọi vật thể có độ tin cậy \> `CONFIDENCE_THRESHOLD`.
    2.  Thư mục `result/` được tạo ra, chứa các thư mục con (ví dụ: `result/person`) là các bản sao của ảnh gốc.
  * Quá trình này có thể mất vài phút đến vài giờ, tùy thuộc vào số lượng ảnh và cấu hình (`DEVICE`, `BATCH_SIZE`...).

### Bước 3: Chạy Trình xem ảnh (Script 2)

Sau khi `db.json` đã được tạo, bạn có thể chạy trình xem:

```bash
python3 view_database.py
```

  * **Script này làm gì?** Nó sẽ đọc file `db.json` và các ảnh trong `source/`.
  * **Kết quả:** Một cửa sổ full-screen sẽ hiện ra.
      * **Thanh trên cùng:** Các Tag (như "Người (person)", "Xe hơi (car)", "Tất Cả Ảnh") để bạn chọn.
      * **Cột bên trái:** Danh sách các file ảnh thuộc Tag bạn vừa chọn.
      * **Khung chính bên phải:** Hiển thị ảnh (đã vẽ các hộp phát hiện) khi bạn bấm vào một tên ảnh.

-----

## ⚙️ Giải thích Chức năng các File

### `sort_photos.py` (Script Phân tích AI)

Đây là "trái tim" xử lý của dự án.

  * **Mục đích:** Xử lý hàng loạt ảnh và tạo ra cơ sở dữ liệu `db.json`.
  * **Logic hoạt động:**
    1.  Tải tất cả cấu hình từ file `.env` (tên mô hình, ngưỡng, thiết bị, tên thư mục, tham số tối ưu).
    2.  Tải mô hình YOLO (`MODEL_NAME`) vào bộ nhớ.
    3.  Kiểm tra sự tồn tại của `DB_FILE_PATH`. Nếu có, hỏi người dùng để "resume" hoặc "chạy mới".
    4.  Nếu "resume", tải CSDL cũ vào bộ nhớ để biết các ảnh đã xử lý.
    5.  Quét thư mục `SOURCE_DIR`, tạo danh sách ảnh cần xử lý (`images_to_process`) bằng cách loại bỏ các ảnh đã có trong CSDL (nếu resume).
    6.  Chia danh sách ảnh thành các lô (`batch`) dựa trên `BATCH_SIZE`.
    7.  Lặp qua từng lô và gọi `model.predict()` với đầy đủ các tham số tối ưu (`device`, `imgsz`, `half`, `workers`).
    8.  Với mỗi kết quả, lặp qua các vật thể (`box`). Nếu `confidence >= CONFIDENCE_THRESHOLD`, lưu vật thể (lớp, % tin cậy, tọa độ) vào CSDL và sao chép ảnh gốc vào thư mục `result/` tương ứng.
    9.  Sau khi lặp xong, ghi đè toàn bộ CSDL (`database_data`) vào file `db.json`.
    10. In ra tổng thời gian xử lý.

### `view_database.py` (Script Trình xem GUI)

Đây là giao diện đồ họa để tương tác với kết quả.

  * **Mục đích:** Cung cấp giao diện trực quan để người dùng xem và duyệt kết quả của AI.
  * **Logic hoạt động:**
    1.  Tải các đường dẫn (`SOURCE_DIR_NAME`, `DB_FILE_NAME`) từ file `.env`.
    2.  Tải toàn bộ file `db.json` vào bộ nhớ (`self.db_data`).
    3.  Tạo một cửa sổ `CustomTkinter` full-screen với layout 3 phần (Tags, Danh sách ảnh, Trình xem ảnh).
    4.  **Xử lý Dữ liệu (`load_data`):** Xây dựng một "bản đồ" (`self.tag_to_images`) từ các Tag (ví dụ: "person") đến danh sách các ảnh chứa tag đó (ví dụ: `['img1.jpg', 'img5.jpg']`). Đồng thời thêm các tag đặc biệt là "*TẤT CẢ*" và "*KHÔNG CÓ TAG*".
    5.  **Hiển thị Tags (`populate_tags_list`):** Lặp qua các tag, tra cứu từ điển `TRANSLATION_DICT` để hiển thị Tiếng Việt (ví dụ: "Người (person)") và tạo các nút bấm ở thanh trên cùng.
    6.  **Sự kiện Bấm Tag (`on_tag_clicked`):**
          * Lưu lại tag vừa chọn (`self.current_selected_tag`).
          * Làm sạch Cột 2 (danh sách ảnh) và **reset thanh cuộn về 0.0**.
          * Lấy danh sách ảnh cho Tag đó và tạo các nút bấm (button) ở Cột 2.
    7.  **Sự kiện Bấm Ảnh (`on_image_clicked`):**
          * Tìm ảnh gốc trong thư mục `source/`.
          * Lấy dữ liệu phát hiện (tọa độ, tên lớp) của ảnh đó từ `self.db_data`.
          * **Lọc thông minh:** Lặp qua các vật thể, chỉ vẽ những vật thể có `det['class'] == self.current_selected_tag` (hoặc vẽ tất cả nếu tag là "*TẤT CẢ*").
          * **Vẽ nhãn:** Dùng Pillow (PIL) để vẽ hộp và nhãn đã được dịch (ví dụ: "Người (person) 95%").
          * Tính toán tỷ lệ (aspect ratio) để hiển thị ảnh vừa vặn trong Khung 3 mà không bị méo.