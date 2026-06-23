import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk, ImageDraw
from algorithms.map_coloring import SEEDS, ADJACENCY, DOMAINS

# Anh xa ten mau sang mau RGB
COLOR_MAP = {
    "Đỏ": (239, 68, 68),          # Do mem mai
    "Xanh lá": (34, 197, 94),     # Xanh la mem mai
    "Vàng": (234, 179, 8),        # Vang mem mai
    "Xanh dương": (59, 130, 246)  # Xanh duong mem mai
}

class MapColoringFrame(tk.Frame):
    def __init__(self, parent, project_dir):
        super().__init__(parent, bg="#f2f4f7")
        self.project_dir = project_dir
        self.map_img_path = os.path.join(self.project_dir, "HCMmap.png")
        self.base_image = None
        self.photo_img = None
        
        if os.path.exists(self.map_img_path):
            try:
                self.base_image = Image.open(self.map_img_path).convert("RGB")
            except Exception as e:
                print(f"Error loading map image: {e}")
        else:
            print(f"Warning: map image not found at {self.map_img_path}")
            
        self.records = []
        self.current_step = 0
        self.after_id = None
        self.is_playing = False
        self.step_delay = 250  # milliseconds
        self.method_title = ""
        
        self.make_ui()

    def make_ui(self):
        # Frame chia lam 2 cot: Trai (Canvas + result + control), Phai (Sidebar process)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=520)
        self.grid_rowconfigure(0, weight=1)
        
        # Vung ben trai
        left_container = tk.Frame(self, bg="#f2f4f7")
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_container.grid_columnconfigure(0, weight=1)
        left_container.grid_rowconfigure(0, weight=5)
        left_container.grid_rowconfigure(1, weight=0, minsize=60)  # Thanh dieu khien
        left_container.grid_rowconfigure(2, weight=0, minsize=180) # Textbox ket qua
        
        # LabelFrame Canvas
        canvas_box = tk.LabelFrame(
            left_container,
            text="Màn hình minh họa tô màu bản đồ TP.HCM",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=8,
            pady=8
        )
        canvas_box.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        canvas_box.grid_columnconfigure(0, weight=1)
        canvas_row = canvas_box.grid_rowconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(canvas_box, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        # Controls panel
        ctrl_panel = tk.Frame(left_container, bg="#f2f4f7")
        ctrl_panel.grid(row=1, column=0, sticky="ew", pady=4)
        
        self.btn_play = ttk.Button(ctrl_panel, text="Tự động chạy (Play)", command=self.play)
        self.btn_play.pack(side="left", padx=4)
        
        self.btn_pause = ttk.Button(ctrl_panel, text="Tạm dừng", command=self.pause, state="disabled")
        self.btn_pause.pack(side="left", padx=4)
        
        self.btn_prev = ttk.Button(ctrl_panel, text="Bước trước", command=self.prev_step)
        self.btn_prev.pack(side="left", padx=4)
        
        self.btn_next = ttk.Button(ctrl_panel, text="Bước tiếp", command=self.next_step)
        self.btn_next.pack(side="left", padx=4)
        
        self.btn_reset = ttk.Button(ctrl_panel, text="Reset", command=self.reset_ui)
        self.btn_reset.pack(side="left", padx=4)
        

        
        # Panel ket qua
        result_box = tk.LabelFrame(
            left_container,
            text="Kết quả tính toán",
            font=("Arial", 12, "bold"),
            bg="white",
            height=180,
            padx=8,
            pady=8
        )
        result_box.grid(row=2, column=0, sticky="nsew", pady=(4, 0))
        result_box.grid_propagate(False)
        result_box.grid_columnconfigure(0, weight=1)
        result_box.grid_rowconfigure(0, weight=1)
        
        self.result_text = tk.Text(
            result_box,
            font=("Consolas", 10),
            wrap="word",
            state="disabled",
            bg="white",
            relief="flat"
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar qua trinh ben phai
        process_box = tk.LabelFrame(
            self,
            text="Quá trình từng bước chạy thuật toán",
            font=("Arial", 12, "bold"),
            bg="white",
            width=520,
            padx=8,
            pady=8
        )
        process_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        process_box.grid_propagate(False)
        process_box.grid_columnconfigure(0, weight=1)
        process_box.grid_rowconfigure(0, weight=1)
        
        self.process_text = tk.Text(
            process_box,
            font=("Consolas", 10),
            wrap="none",
            state="disabled",
            bg="white"
        )
        self.process_text.grid(row=0, column=0, sticky="nsew")
        
        yscroll = ttk.Scrollbar(process_box, orient="vertical", command=self.process_text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.process_text.configure(yscrollcommand=yscroll.set)
        
        xscroll = ttk.Scrollbar(process_box, orient="horizontal", command=self.process_text.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.process_text.configure(xscrollcommand=xscroll.set)

    def update_display(self):
        if not self.base_image:
            self.canvas.delete("all")
            self.canvas.create_text(
                self.canvas.winfo_width()/2,
                self.canvas.winfo_height()/2,
                text="Không tìm thấy ảnh HCMmap.png\nHãy chắc chắn file nằm ở thư mục gốc dự án.",
                font=("Arial", 12, "bold"),
                fill="red",
                justify="center"
            )
            return
            
        # 1. Sao chep anh goc de to màu
        img_copy = self.base_image.copy()
        
        # 2. To màu cac quan da gan o buoc hien tai
        if self.records and self.current_step < len(self.records):
            record = self.records[self.current_step]
            assignment = record.get("assignment", {})
            for district, color_name in assignment.items():
                if district in SEEDS and color_name in COLOR_MAP:
                    seed = SEEDS[district]
                    color = COLOR_MAP[color_name]
                    # Thuc hien loang màu tai toa do hat giong voi nguong 18 an toan (tranh nghen co chai o Q11 va Q5)
                    ImageDraw.floodfill(img_copy, seed, color, thresh=18)
                    
        # 3. Thay doi kich thuoc de vua van voi canvas (giu nguyen ti le aspect ratio)
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w <= 1:
            canvas_w = 800
        if canvas_h <= 1:
            canvas_h = 500
            
        img_w, img_h = img_copy.size
        ratio = min(canvas_w / img_w, canvas_h / img_h)
        new_w = int(img_w * ratio)
        new_h = int(img_h * ratio)
        
        if hasattr(Image, "Resampling"):
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
            
        resized = img_copy.resize((new_w, new_h), resample)
        self.photo_img = ImageTk.PhotoImage(resized)
        
        # 4. Ve anh len canvas
        self.canvas.delete("all")
        x = (canvas_w - new_w) / 2
        y = (canvas_h - new_h) / 2
        self.canvas.create_image(x, y, image=self.photo_img, anchor="nw")
        
        # Ve tieu de thuat toan va buoc chay
        step_title = f"{self.method_title} - Bước {self.current_step + 1}/{len(self.records)}" if self.records else self.method_title
        self.canvas.create_text(
            20, 25,
            text=step_title,
            font=("Arial", 12, "bold"),
            fill="#0f172a",
            anchor="w"
        )

    def update_logs(self):
        self.process_text.config(state="normal")
        self.process_text.delete("1.0", "end")
        
        for i in range(self.current_step + 1):
            if i < len(self.records):
                self.process_text.insert("end", self.records[i]["log"])
                
        self.process_text.see("end")
        self.process_text.config(state="disabled")

    def set_records(self, method_title, records):
        self.method_title = method_title
        self.records = records
        self.current_step = 0
        self.is_playing = False
        
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None
            
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled")
        
        self.update_display()
        self.update_logs()
        self.set_result(f"Sẵn sàng chạy mô phỏng {self.method_title}.\nNhấp Play hoặc Bước tiếp để bắt đầu.")

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", text)
        self.result_text.config(state="disabled")

    def play(self):
        if not self.records:
            return
        self.is_playing = True
        self.btn_play.config(state="disabled")
        self.btn_pause.config(state="normal")
        self.run_animation()

    def pause(self):
        self.is_playing = False
        self.btn_play.config(state="normal")
        self.btn_pause.config(state="disabled")
        if self.after_id:
            self.after_cancel(self.after_id)
            self.after_id = None

    def run_animation(self):
        if not self.is_playing:
            return
            
        if self.current_step < len(self.records) - 1:
            self.current_step += 1
            self.update_display()
            self.update_logs()
            self.after_id = self.after(self.step_delay, self.run_animation)
        else:
            self.pause()
            final_record = self.records[-1]
            self.set_result(final_record["log"])

    def next_step(self):
        self.pause()
        if self.records and self.current_step < len(self.records) - 1:
            self.current_step += 1
            self.update_display()
            self.update_logs()
            if self.current_step == len(self.records) - 1:
                self.set_result(self.records[-1]["log"])
            else:
                self.set_result(f"Đã chuyển sang Bước {self.current_step + 1}")

    def prev_step(self):
        self.pause()
        if self.records and self.current_step > 0:
            self.current_step -= 1
            self.update_display()
            self.update_logs()
            self.set_result(f"Quay lại Bước {self.current_step + 1}")

    def reset_ui(self):
        self.pause()
        self.current_step = 0
        self.update_display()
        self.update_logs()
        self.set_result("Đã reset về trạng thái ban đầu.")



    def on_canvas_configure(self, event):
        self.update_display()
