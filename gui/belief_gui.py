import tkinter as tk
from tkinter import ttk
from algorithms.searching_in_complex_environment.belief_state_search import SIZE


class BeliefFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f2f4f7")
        self.records = []
        self.current_step = 0
        self.after_id = None
        self.is_playing = False
        self.step_delay = 400
        self.method_title = ""
        self.make_ui()

    def make_ui(self):
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=520)
        self.grid_rowconfigure(0, weight=1)

        left = tk.Frame(self, bg="#f2f4f7")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_columnconfigure(0, weight=1)
        left.grid_rowconfigure(0, weight=5)
        left.grid_rowconfigure(1, weight=0, minsize=60)
        left.grid_rowconfigure(2, weight=0, minsize=180)

        canvas_box = tk.LabelFrame(
            left, text="Belief State - Máy Hút Bụi 3x3",
            font=("Arial", 12, "bold"), bg="white", padx=8, pady=8
        )
        canvas_box.grid(row=0, column=0, sticky="nsew", pady=(0, 4))
        canvas_box.grid_columnconfigure(0, weight=1)
        canvas_box.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(canvas_box, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        ctrl = tk.Frame(left, bg="#f2f4f7")
        ctrl.grid(row=1, column=0, sticky="ew", pady=4)

        self.btn_play  = ttk.Button(ctrl, text="Tự động chạy (Play)", command=self.play)
        self.btn_pause = ttk.Button(ctrl, text="Tạm dừng", command=self.pause, state="disabled")
        self.btn_prev  = ttk.Button(ctrl, text="Bước trước", command=self.prev_step)
        self.btn_next  = ttk.Button(ctrl, text="Bước tiếp", command=self.next_step)
        self.btn_reset = ttk.Button(ctrl, text="Reset", command=self.reset_ui)

        for btn in [self.btn_play, self.btn_pause, self.btn_prev, self.btn_next, self.btn_reset]:
            btn.pack(side="left", padx=4)

        result_box = tk.LabelFrame(
            left, text="Kết quả tính toán",
            font=("Arial", 12, "bold"), bg="white", height=180, padx=8, pady=8
        )
        result_box.grid(row=2, column=0, sticky="nsew", pady=(4, 0))
        result_box.grid_propagate(False)
        result_box.grid_columnconfigure(0, weight=1)
        result_box.grid_rowconfigure(0, weight=1)

        self.result_text = tk.Text(
            result_box, font=("Consolas", 10), wrap="word",
            state="disabled", bg="white", relief="flat"
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")

        process_box = tk.LabelFrame(
            self, text="Quá trình từng bước chạy thuật toán",
            font=("Arial", 12, "bold"), bg="white", width=520, padx=8, pady=8
        )
        process_box.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        process_box.grid_propagate(False)
        process_box.grid_columnconfigure(0, weight=1)
        process_box.grid_rowconfigure(0, weight=1)

        self.process_text = tk.Text(
            process_box, font=("Consolas", 10), wrap="none",
            state="disabled", bg="white"
        )
        self.process_text.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(process_box, orient="vertical", command=self.process_text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.process_text.configure(yscrollcommand=yscroll.set)

        xscroll = ttk.Scrollbar(process_box, orient="horizontal", command=self.process_text.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.process_text.configure(xscrollcommand=xscroll.set)

    def update_display(self):
        self.canvas.delete("all")
        if not self.records:
            return

        record = self.records[self.current_step]
        belief = record["belief"]
        action = record["action"]
        n = len(belief)

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1: w = 600
        if h <= 1: h = 400

        robot_prob = {
            (r, c): sum(1 for pos, _ in belief if pos == (r, c)) / n
            for r in range(SIZE) for c in range(SIZE)
        }
        dirty_prob = {
            (r, c): sum(1 for _, grid in belief if grid[r][c] == 1) / n
            for r in range(SIZE) for c in range(SIZE)
        }

        cell = min(int(w * 0.65 / SIZE), int(h * 0.65 / SIZE))
        cell = max(cell, 70)
        grid_w = cell * SIZE
        grid_h = cell * SIZE
        x0 = (w - grid_w) / 2
        y0 = 65

        step_label = (
            f"{self.method_title} - Bước {self.current_step + 1}/{len(self.records)} "
            f"| Action: {action} | Belief = {n} trạng thái"
        )
        self.canvas.create_text(w / 2, 30, text=step_label, font=("Arial", 12, "bold"), fill="#1e293b")

        for r in range(SIZE):
            for c in range(SIZE):
                x = x0 + c * cell
                y = y0 + r * cell
                rp = robot_prob[(r, c)]
                dp = dirty_prob[(r, c)]

                if rp > 0 and dp > 0:
                    fill = "#fecaca"   # robot + bẩn -> đỏ nhạt
                elif rp > 0:
                    fill = "#bfdbfe"   # có robot, sạch -> xanh dương
                elif dp > 0.6:
                    fill = "#fef3c7"   # nhiều khả năng bẩn -> vàng
                elif dp > 0:
                    fill = "#fef9c3"   # ít khả năng bẩn -> vàng nhạt
                else:
                    fill = "#d1fae5"   # chắc chắn sạch -> xanh lá

                self.canvas.create_rectangle(
                    x, y, x + cell, y + cell,
                    fill=fill, outline="#64748b", width=2
                )
                self.canvas.create_text(
                    x + cell / 2, y + cell / 2 - 12,
                    text=f"R: {rp * 100:.0f}%",
                    font=("Arial", 10, "bold"), fill="#1e40af"
                )
                self.canvas.create_text(
                    x + cell / 2, y + cell / 2 + 12,
                    text=f"Bẩn: {dp * 100:.0f}%",
                    font=("Arial", 10), fill="#92400e"
                )

        legend_y = y0 + grid_h + 20
        self.canvas.create_text(
            w / 2, legend_y,
            text="Xanh dương=Robot | Vàng=Có thể bẩn | Xanh lá=Chắc sạch | Đỏ=Robot+Bẩn",
            font=("Arial", 9), fill="#6b7280"
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
        self.set_result(f"Sẵn sàng chạy mô phỏng: {self.method_title}\nNhấn Play hoặc Bước tiếp để bắt đầu.")

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
            self.set_result(self.records[-1]["log"])

    def next_step(self):
        self.pause()
        if self.records and self.current_step < len(self.records) - 1:
            self.current_step += 1
            self.update_display()
            self.update_logs()
            if self.current_step == len(self.records) - 1:
                self.set_result(self.records[-1]["log"])

    def prev_step(self):
        self.pause()
        if self.records and self.current_step > 0:
            self.current_step -= 1
            self.update_display()
            self.update_logs()

    def reset_ui(self):
        self.pause()
        self.current_step = 0
        self.update_display()
        self.update_logs()
        self.set_result("Đã reset về trạng thái ban đầu.")

    def on_canvas_configure(self, event):
        self.update_display()
