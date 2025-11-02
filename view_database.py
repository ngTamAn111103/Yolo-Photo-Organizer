import os
import json
import customtkinter as ctk
from dotenv import load_dotenv # <--- Thêm vào
from PIL import Image, ImageDraw, ImageFont
# --- 1. TẢI CẤU HÌNH TỪ .ENV ---
load_dotenv() # <--- Thêm vào

# Lấy đường dẫn cơ sở của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lấy các hằng số từ file .env
SOURCE_DIR_NAME = os.getenv("SOURCE_DIR_NAME", "source")
DB_FILE_NAME = os.getenv("DB_FILE_NAME", "database.json")

# Xây dựng các đường dẫn tuyệt đối
SOURCE_DIR = os.path.join(BASE_DIR, SOURCE_DIR_NAME)
DB_FILE_PATH = os.path.join(BASE_DIR, DB_FILE_NAME)

# Cấu hình giao diện (không cần .env)
BOX_COLOR = "red"
TEXT_COLOR = "white"
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png')
TRANSLATION_DICT = {
    # Người & Động vật
    "person": "Người",
    "bird": "Chim",
    "cat": "Mèo",
    "dog": "Chó",
    "horse": "Ngựa",
    "sheep": "Cừu",
    "cow": "Bò",
    "elephant": "Voi",
    "bear": "Gấu",
    "zebra": "Ngựa vằn",
    "giraffe": "Hươu cao cổ",
    
    # Phương tiện
    "bicycle": "Xe đạp",
    "car": "Xe hơi",
    "motorcycle": "Xe máy",
    "airplane": "Máy bay",
    "bus": "Xe buýt",
    "train": "Tàu hỏa",
    "truck": "Xe tải",
    "boat": "Thuyền",

    # Vật dụng đường phố
    "traffic light": "Đèn giao thông",
    "fire hydrant": "Trụ cứu hỏa",
    "stop sign": "Biển báo dừng",
    "parking meter": "Máy đo đỗ xe",
    "bench": "Ghế dài",

    # Đồ dùng cá nhân
    "backpack": "Ba lô",
    "umbrella": "Ô/Dù",
    "handbag": "Túi xách",
    "tie": "Cà vạt",
    "suitcase": "Va li",

    # Thể thao
    "frisbee": "Đĩa ném",
    "skis": "Ván trượt tuyết (dài)",
    "snowboard": "Ván trượt tuyết (ngắn)",
    "sports ball": "Bóng thể thao",
    "kite": "Diều",
    "baseball bat": "Gậy bóng chày",
    "baseball glove": "Găng tay bóng chày",
    "skateboard": "Ván trượt",
    "surfboard": "Ván lướt sóng",
    "tennis racket": "Vợt tennis",

    # Dụng cụ ăn uống & Đồ ăn
    "bottle": "Chai",
    "wine glass": "Ly rượu vang",
    "cup": "Cốc",
    "fork": "Nĩa",
    "knife": "Dao",
    "spoon": "Thìa",
    "bowl": "Bát/Tô",
    "banana": "Chuối",
    "apple": "Táo",
    "sandwich": "Bánh mỳ kẹp",
    "orange": "Cam",
    "broccoli": "Bông cải xanh",
    "carrot": "Cà rốt",
    "hot dog": "Xúc xích",
    "pizza": "Pizza",
    "donut": "Bánh donut",
    "cake": "Bánh ngọt",

    # Nội thất
    "chair": "Ghế",
    "couch": "Ghế sofa",
    "potted plant": "Cây trồng chậu",
    "bed": "Giường",
    "dining table": "Bàn ăn",
    "toilet": "Bồn cầu",

    # Điện tử
    "tv": "TV",
    "laptop": "Máy tính xách tay",
    "mouse": "Chuột máy tính",
    "remote": "Điều khiển từ xa",
    "keyboard": "Bàn phím",
    "cell phone": "Điện thoại",

    # Đồ gia dụng
    "microwave": "Lò vi sóng",
    "oven": "Lò nướng",
    "toaster": "Máy nướng bánh mỳ",
    "sink": "Bồn rửa",
    "refrigerator": "Tủ lạnh",

    # Khác
    "book": "Sách",
    "clock": "Đồng hồ",
    "vase": "Bình hoa",
    "scissors": "Kéo",
    "teddy bear": "Gấu bông",
    "hair drier": "Máy sấy tóc",
    "toothbrush": "Bàn chải"
}
class ImageBrowserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- YÊU CẦU 1: FULL MÀN HÌNH ---
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}+0+0")
        self.title("Trình duyệt Ảnh YOLO (Nâng cấp)")
        
        self.db_data = {}           
        self.tag_to_images = {}    
        self.current_selected_tag = None 
        
        # --- YÊU CẦU 2: LAYOUT MỚI ---
        # Cấu hình Layout (2 hàng, 2 cột)
        # Hàng 0: Tags (chiều cao cố định)
        # Hàng 1: Nội dung (chiếm hết phần còn lại)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1)
        # Cột 0: Danh sách ảnh (rộng 1 phần)
        # Cột 1: Trình xem ảnh (rộng 3 phần)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        
        # --- Hàng 0: Thanh Tags (cuộn ngang) ---
        self.frame_tags_container = ctk.CTkFrame(self, height=60) # Khung chứa
        self.frame_tags_container.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="new")
        
        ctk.CTkLabel(self.frame_tags_container, text="TAGS:", font=("Roboto", 16, "bold")).pack(side="left", padx=10)
        
        self.scrollable_frame_tags = ctk.CTkScrollableFrame(self.frame_tags_container, orientation="horizontal")
        self.scrollable_frame_tags.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Hàng 1, Cột 0: Danh sách Ảnh ---
        self.frame_images = ctk.CTkFrame(self)
        self.frame_images.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.label_images_title = ctk.CTkLabel(self.frame_images, text="CHỌN 1 TAG", font=("Roboto", 16, "bold"))
        self.label_images_title.pack(pady=10)
        
        self.scrollable_frame_images = ctk.CTkScrollableFrame(self.frame_images)
        self.scrollable_frame_images.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Hàng 1, Cột 1: Trình xem Ảnh ---
        self.frame_viewer = ctk.CTkFrame(self)
        self.frame_viewer.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        
        self.image_label = ctk.CTkLabel(self.frame_viewer, text="Chọn một ảnh để xem", text_color="gray")
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Tải dữ liệu ---
        self.load_data()
        self.populate_tags_list()

    def load_data(self):
        """Tải database.json và xử lý dữ liệu (không đổi)."""
        print("Đang tải cơ sở dữ liệu...")
        try:
            with open(DB_FILE_PATH, 'r', encoding='utf-8') as f:
                self.db_data = json.load(f)
        except FileNotFoundError:
            print(f"LỖI: Không tìm thấy file {DB_FILE_PATH}")
            self.image_label.configure(text=f"LỖI: Không tìm thấy file {DB_FILE_PATH}")
            return
        except json.JSONDecodeError:
            print(f"LỖI: File {DB_FILE_PATH} bị hỏng hoặc rỗng.")
            self.image_label.configure(text=f"LỖI: File {DB_FILE_PATH} bị hỏng.")
            return

        print("Đang xử lý dữ liệu và quét ảnh...")
        
        all_images_in_folder = []
        if os.path.exists(SOURCE_DIR):
             all_images_in_folder = [f for f in os.listdir(SOURCE_DIR) if f.lower().endswith(SUPPORTED_EXTENSIONS)]
        else:
            print(f"LỖI: Không tìm thấy thư mục ảnh nguồn: {SOURCE_DIR}")
            self.image_label.configure(text=f"LỖI: Không tìm thấy thư mục {SOURCE_DIR}")
            return
            
        tagged_images = set() 
        temp_tag_map = {}

        for image_name, detections in self.db_data.items():
            if image_name not in all_images_in_folder:
                print(f"Cảnh báo: Ảnh {image_name} có trong JSON nhưng không có trong thư mục 'source'.")
                continue 
            
            tagged_images.add(image_name)
            unique_classes = set(d['class'] for d in detections)
            
            for tag in unique_classes:
                if tag not in temp_tag_map:
                    temp_tag_map[tag] = []
                temp_tag_map[tag].append(image_name)

        untagged_list = []
        for image_name in all_images_in_folder:
            if image_name not in tagged_images:
                untagged_list.append(image_name)

        sorted_tags = sorted(temp_tag_map.keys())
        self.tag_to_images["_TẤT CẢ_"] = all_images_in_folder
        
        self.tag_to_images["_KHÔNG CÓ TAG_"] = untagged_list
        for tag in sorted_tags:
            self.tag_to_images[tag] = temp_tag_map[tag]
        
        print(f"Tải xong! Tìm thấy {len(self.tag_to_images) - 1} tags và {len(untagged_list)} ảnh không có tag.")

    def populate_tags_list(self):
        """Hiển thị danh sách các nút tag (Sửa để pack ngang)."""
        # Sắp xếp lại để _TẤT CẢ_ và _KHÔNG CÓ TAG_ luôn ở đầu
        all_tags = list(self.tag_to_images.keys())
        if "_TẤT CẢ_" in all_tags:
            all_tags.remove("_TẤT CẢ_")
            all_tags.insert(0, "_TẤT CẢ_")
        if "_KHÔNG CÓ TAG_" in all_tags:
            all_tags.remove("_KHÔNG CÓ TAG_")
            all_tags.insert(1, "_KHÔNG CÓ TAG_")
            
        for tag in all_tags:
            
            # --- Logic dịch thuật ---
            display_text = tag # Mặc định
            
            # --- SỬA ĐỔI 3: Thêm dịch cho tag mới ---
            if tag == "_TẤT CẢ_":
                display_text = "Tất Cả Ảnh"
            # --- HẾT SỬA ĐỔI 3 ---
            elif tag == "_KHÔNG CÓ TAG_":
                display_text = "Không có Tag"
            elif tag in TRANSLATION_DICT:
                # Nếu có, hiển thị: "Tiếng Việt (english)"
                display_text = f"{TRANSLATION_DICT[tag]} ({tag})"
            # --- Hết logic dịch thuật ---

            button = ctk.CTkButton(
                self.scrollable_frame_tags,
                text=display_text, # <--- Dùng text đã dịch
                command=lambda t=tag: self.on_tag_clicked(t) # Command vẫn dùng tag gốc
            )
            button.pack(side="left", padx=5, pady=2)

    def on_tag_clicked(self, tag_name):
        """
        Làm sạch và hiển thị danh sách ảnh (Thêm dịch cho tiêu đề).
        Không có preview (Dành cho danh sách ảnh quá nhiều)
        """
        
        # --- SỬA ĐỔI 4: Lưu lại tag vừa bấm ---
        self.current_selected_tag = tag_name
        # --- HẾT SỬA ĐỔI 4 ---
        
        # --- Logic dịch thuật cho tiêu đề ---
        display_title = tag_name
        if tag_name == "_TẤT CẢ_":
            display_title = "Tất Cả Ảnh"
        elif tag_name == "_KHÔNG CÓ TAG_":
            display_title = "Không có Tag"
        elif tag_name in TRANSLATION_DICT:
            display_title = f"{TRANSLATION_DICT[tag_name]} ({tag_name})"
        
        self.label_images_title.configure(text=f"Ảnh cho tag: {display_title}")
        # --- Hết logic dịch thuật ---

        # self.scrollable_frame_images.set(0.0)

        for widget in self.scrollable_frame_images.winfo_children():
            widget.destroy()
        
        # Logic tra cứu vẫn dùng tag_name gốc (tiếng Anh)
        image_list = self.tag_to_images[tag_name] 
        
        for image_name in image_list:
            button = ctk.CTkButton(
                self.scrollable_frame_images, 
                text=image_name,
                fg_color="transparent", 
                command=lambda img=image_name: self.on_image_clicked(img)
            )
            button.pack(fill="x", padx=5, pady=2)
    # def on_tag_clicked(self, tag_name):
    #     """
    #     Làm sạch và hiển thị danh sách ảnh (Thêm dịch cho tiêu đề).
    #     Có preview (Dành cho danh sách có ít ảnh)
    #     """
        
    #     # --- Logic dịch thuật cho tiêu đề ---
    #     display_title = tag_name
    #     if tag_name == "_KHÔNG CÓ TAG_":
    #         display_title = "Không có Tag"
    #     elif tag_name in TRANSLATION_DICT:
    #         display_title = f"{TRANSLATION_DICT[tag_name]} ({tag_name})"
        
    #     self.label_images_title.configure(text=f"Ảnh cho tag: {display_title}")
    #     # --- Hết logic dịch thuật ---

    #     # --- SỬA ĐỔI 1: Xóa widget cũ và tạo danh sách giữ tham chiếu ảnh ---
    #     # Chúng ta cần danh sách này để giữ cho các đối tượng ảnh
    #     # không bị Python tự động xóa khỏi bộ nhớ (garbage collection)
    #     self.thumbnail_images = [] 
    #     for widget in self.scrollable_frame_images.winfo_children():
    #         widget.destroy()
        
    #     # Logic tra cứu vẫn dùng tag_name gốc (tiếng Anh)
    #     image_list = self.tag_to_images[tag_name] 
        
    #     # --- SỬA ĐỔI 2: ĐỊNH NGHĨA KÍCH THƯỚC PREVIEW ---
    #     THUMB_SIZE = (64, 64) # Kích thước ảnh preview (cao 64, rộng 64)

    #     for image_name in image_list:
            
    #         # --- SỬA ĐỔI 3: TẢI VÀ TẠO THUMBNAIL ---
    #         thumbnail_image = None # Mặc định là không có ảnh
    #         try:
    #             # Mở ảnh gốc từ thư mục 'source'
    #             image_path = os.path.join(SOURCE_DIR, image_name)
    #             pil_image = Image.open(image_path)
                
    #             # Thu nhỏ ảnh (giữ nguyên tỷ lệ)
    #             pil_image.thumbnail(THUMB_SIZE) 
                
    #             # Tạo đối tượng ảnh cho CustomTkinter
    #             ctk_thumb = ctk.CTkImage(light_image=pil_image, size=THUMB_SIZE)
                
    #             # Thêm vào danh sách để giữ tham chiếu
    #             self.thumbnail_images.append(ctk_thumb) 
    #             thumbnail_image = ctk_thumb

    #         except Exception as e:
    #             print(f"Lỗi khi tạo thumbnail cho {image_name}: {e}")
    #             # Nếu lỗi, thumbnail_image vẫn là None, nút sẽ không có ảnh
    #         # --- KẾT THÚC SỬA ĐỔI 3 ---

    #         button = ctk.CTkButton(
    #             self.scrollable_frame_images, 
    #             text=image_name,
    #             fg_color="transparent", 
    #             command=lambda img=image_name: self.on_image_clicked(img),
                
    #             # --- SỬA ĐỔI 4: THÊM ẢNH VÀO NÚT ---
    #             image=thumbnail_image,  # Thêm ảnh preview
    #             compound="left",      # Đặt ảnh ở bên trái của chữ
    #             anchor="w"            # Căn lề chữ về bên trái (West)
    #             # --- KẾT THÚC SỬA ĐỔI 4 ---
    #         )
    #         button.pack(fill="x", padx=5, pady=2)
    

    def on_image_clicked(self, image_name):
        """Hiển thị ảnh (Sửa lỗi bóp méo)."""
        print(f"Đang tải ảnh: {image_name}")
        
        image_path = os.path.join(SOURCE_DIR, image_name)
        if not os.path.exists(image_path):
            self.image_label.configure(text=f"LỖI: Không tìm thấy file {image_name}")
            return
            
        detections = self.db_data.get(image_name, [])
        pil_image = Image.open(image_path).convert("RGBA")
        
        # Vẽ bounding box (nếu có)
        if detections:
            draw = ImageDraw.Draw(pil_image)
            try:
                # (Font loading giữ nguyên)
                font_path = "/System/Library/Fonts/Helvetica.ttc"
                font = ImageFont.truetype(font_path, 100)
            except IOError:
                print("Không tìm thấy font Helvetica, dùng font mặc định.")
                font = ImageFont.load_default(100)

            for det in detections:
                # --- THÊM LOGIC LỌC ---
                # Chỉ vẽ khi:
                # 1. Tag đang chọn là "_TẤT CẢ_" (luôn vẽ)
                # 2. Hoặc Lớp (class) của vật thể khớp với tag đang chọn
                
                if (self.current_selected_tag == "_TẤT CẢ_" or 
                    det['class'] == self.current_selected_tag):
                    
                    # (Toàn bộ code vẽ bên dưới được thụt vào trong khối IF này)
                    box = det['box']
                    original_class = det['class']
                    display_class = original_class # Mặc định
                    
                    if original_class in TRANSLATION_DICT:
                        # Tạo định dạng: "Tiếng Việt (english)"
                        display_class = f"{TRANSLATION_DICT[original_class]} ({original_class})"
                    
                    # Thêm độ tin cậy vào nhãn
                    label = f"{display_class} ({det['confidence']:.0%})"

                    draw.rectangle(box, outline=BOX_COLOR, width=5)
                    text_y = box[1] - 15
                    if text_y < 0: text_y = 0
                    text_bbox = draw.textbbox((box[0], text_y), label, font=font)
                    draw.rectangle(text_bbox, fill=BOX_COLOR)
                    draw.text((box[0], text_y), label, fill=TEXT_COLOR, font=font)
                
                # --- HẾT LOGIC LỌC ---
        
        # --- YÊU CẦU 3: SỬA LỖI BÓP MÉO ẢNH ---
        orig_width, orig_height = pil_image.size

        # Lấy kích thước của khung chứa ảnh (trừ 1 chút padding)
        # update_idletasks() để đảm bảo tkinter đã tính đúng kích thước
        self.frame_viewer.update_idletasks() 
        max_width = self.frame_viewer.winfo_width() - 20
        max_height = self.frame_viewer.winfo_height() - 20

        # Nếu kích thước không hợp lệ (lần đầu), dùng giá trị dự phòng
        if max_width < 1 or max_height < 1:
            max_width, max_height = 800, 600

        # Tính toán tỷ lệ để giữ đúng aspect ratio
        ratio = min(max_width / orig_width, max_height / orig_height)
        
        new_width = int(orig_width * ratio)
        new_height = int(orig_height * ratio)

        # Tạo CTkImage với kích thước MỚI (đã tính toán)
        ctk_image = ctk.CTkImage(
            light_image=pil_image,
            size=(new_width, new_height) # <-- Kích thước động
        )
        
        self.image_label.configure(image=ctk_image, text="")

# --- Chạy ứng dụng ---
if __name__ == "__main__":
    app = ImageBrowserApp()
    app.mainloop()