# Giao dien Tkinter cho bai May Hut Bui

import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk

from config import (
    SIZE, START_GRID, START_POS, GOAL_GRID,
    MAX_SHOW_RECORDS, STEP_DELAY
)
from node import Node, is_goal, heuristic, path_to_root, matrix_text, matrix_short
from algorithms import search


class CollapsibleFrame(tk.Frame):
    def __init__(self, parent, title="", start_expanded=False, **kwargs):
        super().__init__(parent, bg="#f2f4f7", **kwargs)
        self.title = title
        self.is_expanded = start_expanded

        self.toggle_btn = tk.Button(
            self,
            text=f"▼  {self.title}" if self.is_expanded else f"▶  {self.title}",
            font=("Arial", 10, "bold"),
            anchor="w",
            relief="flat",
            bg="#cbd5e1",
            fg="#0f172a",
            activebackground="#94a3b8",
            activeforeground="#0f172a",
            padx=8,
            pady=6,
            command=self.toggle
        )
        self.toggle_btn.pack(fill="x", pady=2)

        self.sub_frame = tk.Frame(self, bg="#f2f4f7")
        if self.is_expanded:
            self.sub_frame.pack(fill="x", padx=4, pady=2)

    def toggle(self):
        if self.is_expanded:
            self.sub_frame.pack_forget()
            self.toggle_btn.config(text=f"▶  {self.title}", bg="#cbd5e1")
            self.is_expanded = False
        else:
            self.sub_frame.pack(fill="x", padx=4, pady=2)
            self.toggle_btn.config(text=f"▼  {self.title}", bg="#94a3b8")
            self.is_expanded = True


class VacuumApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("May hut bui")
        self.geometry("1440x800")
        self.minsize(1180, 680)
        self.configure(bg="#f2f4f7")

        self.records = []
        self.display_records = []
        self.was_record_limited = False
        self.goal_node = None
        self.search_status = "failure"
        self.current_title = ""
        self.after_id = None
        self.shown_frontier_names = set()

        self.current_node = None
        self.current_state_title = ""
        self.current_state_note = ""
        self.map_coloring_frame = None
        self.belief_frame = None

        # Load images
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.robot_img_path = os.path.join(self.project_dir, "robot_vacuum_cleaner.png")
        self.stain_img_path = os.path.join(self.project_dir, "stain.png")
        
        self.robot_pil = None
        self.stain_pil = None
        if os.path.exists(self.robot_img_path):
            try:
                self.robot_pil = Image.open(self.robot_img_path)
            except Exception as e:
                print(f"Error loading robot image: {e}")
        if os.path.exists(self.stain_img_path):
            try:
                self.stain_pil = Image.open(self.stain_img_path)
            except Exception as e:
                print(f"Error loading stain image: {e}")
                
        self.img_cache = {}

        self.make_ui()
        self.draw_start_screen()

    def get_cached_image(self, img_type, cell_size):
        key = (img_type, cell_size)
        if key in self.img_cache:
            return self.img_cache[key]
        
        pil_img = self.robot_pil if img_type == "robot" else self.stain_pil
        if pil_img is None:
            return None
        
        try:
            # Chuyển đổi ảnh sang RGBA để kích hoạt thuật toán khử răng cưa Lanczos chất lượng cao khi resize
            # (Ảnh gốc đang ở hệ màu Palette "P" nên resize mặc định dùng Nearest Neighbor gây vỡ hạt)
            pil_img = pil_img.convert("RGBA")
            
            # Resize image to fit nicely within the cell
            size = int(cell_size * 0.85)
            if hasattr(Image, "Resampling"):
                resample = Image.Resampling.LANCZOS
            elif hasattr(Image, "LANCZOS"):
                resample = Image.LANCZOS
            else:
                resample = Image.ANTIALIAS
                
            resized = pil_img.resize((size, size), resample)
            photo_img = ImageTk.PhotoImage(resized)
            self.img_cache[key] = photo_img
            return photo_img
        except Exception as e:
            print(f"Error resizing image {img_type}: {e}")
            return None

    # ------------------------------------------------------------------
    # Xay dung giao dien
    # ------------------------------------------------------------------

    def make_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Arial", 10, "bold"), padding=(8, 8))

        main = tk.Frame(self, bg="#f2f4f7", padx=16, pady=16)
        main.pack(fill="both", expand=True)
        self.main_frame = main

        main.grid_columnconfigure(0, weight=0, minsize=230)
        main.grid_columnconfigure(1, weight=2)
        main.grid_columnconfigure(2, weight=0, minsize=520)
        main.grid_rowconfigure(0, weight=1)

        # Cot nut ben trai
        left = tk.Frame(main, bg="#f2f4f7", width=230)
        left.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        left.pack_propagate(False)

        # Nhom 1: Uninformed Search (Mo rong mac dinh)
        uninformed_sec = CollapsibleFrame(left, title="Uninformed Search", start_expanded=True)
        uninformed_sec.pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="BFS cách 1",           command=lambda: self.run_algo("BFS", 1)).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="BFS cách 2",           command=lambda: self.run_algo("BFS", 2)).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="DFS cách 1",           command=lambda: self.run_algo("DFS", 1)).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="DFS cách 2",           command=lambda: self.run_algo("DFS", 2)).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="UCS",                  command=lambda: self.run_algo("UCS")).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="IDS cách 1",           command=lambda: self.run_algo("IDS", 1)).pack(fill="x", pady=2)
        ttk.Button(uninformed_sec.sub_frame, text="IDS cách 2",           command=lambda: self.run_algo("IDS", 2)).pack(fill="x", pady=2)

        # Nhom 2: Informed Search (Thu gon mac dinh)
        informed_sec = CollapsibleFrame(left, title="Informed Search", start_expanded=False)
        informed_sec.pack(fill="x", pady=2)
        ttk.Button(informed_sec.sub_frame, text="Greedy",               command=lambda: self.run_algo("Greedy")).pack(fill="x", pady=2)
        ttk.Button(informed_sec.sub_frame, text="A*",                   command=lambda: self.run_algo("A*")).pack(fill="x", pady=2)
        ttk.Button(informed_sec.sub_frame, text="IDA*",                 command=lambda: self.run_algo("IDA*")).pack(fill="x", pady=2)

        # Nhom 3: Local Search (Thu gon mac dinh)
        local_sec = CollapsibleFrame(left, title="Local Search", start_expanded=False)
        local_sec.pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Simple Hill Climbing", command=lambda: self.run_algo("Simple Hill Climbing")).pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Steepest Ascent Hill", command=lambda: self.run_algo("Steepest Ascent Hill")).pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Stochastic Hill",      command=lambda: self.run_algo("Stochastic Hill")).pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Random Restart Hill",  command=lambda: self.run_algo("Random Restart Hill")).pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Local Beam Search",     command=lambda: self.run_algo("Local Beam Search")).pack(fill="x", pady=2)
        ttk.Button(local_sec.sub_frame, text="Simulated Annealing",  command=lambda: self.run_algo("Simulated Annealing")).pack(fill="x", pady=2)

        # Nhom 4: Search in Complex Environments (Thu gon mac dinh)
        complex_sec = CollapsibleFrame(left, title="Searching in complex environments", start_expanded=False)
        complex_sec.pack(fill="x", pady=2)
        ttk.Button(complex_sec.sub_frame, text="AND-OR Graph Search", command=lambda: self.run_algo("AND-OR Graph Search")).pack(fill="x", pady=2)
        ttk.Button(complex_sec.sub_frame, text="No Observation", command=lambda: self.run_belief("No Observation")).pack(fill="x", pady=2)
        ttk.Button(complex_sec.sub_frame, text="Partial Observation", command=lambda: self.run_belief("Partial Observation")).pack(fill="x", pady=2)

        # Nhom 5: Constraint satisfaction problems (Thu gon mac dinh)
        csp_sec = CollapsibleFrame(left, title="Constraint satisfaction problems", start_expanded=False)
        csp_sec.pack(fill="x", pady=2)
        ttk.Button(csp_sec.sub_frame, text="Backtracking (Tô màu)", command=lambda: self.run_map_coloring("Map Coloring - Backtracking")).pack(fill="x", pady=2)
        ttk.Button(csp_sec.sub_frame, text="Forward Checking (Tô màu)", command=lambda: self.run_map_coloring("Map Coloring - Forward Checking")).pack(fill="x", pady=2)

        # Nut Reset dat ben duoi cung
        ttk.Button(left, text="Reset Bản Đồ",         command=self.reset_app).pack(fill="x", pady=(24, 4))

        # Cot giua
        middle = tk.Frame(main, bg="#f2f4f7")
        middle.grid(row=0, column=1, sticky="nsew")
        self.middle_frame = middle
        middle.grid_columnconfigure(0, weight=1)
        middle.grid_rowconfigure(0, weight=5)
        middle.grid_rowconfigure(1, weight=0, minsize=240)

        screen_box = tk.LabelFrame(
            middle,
            text="Màn hình minh họa hoạt động",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=8,
            pady=8
        )
        screen_box.grid(row=0, column=0, sticky="nsew")
        screen_box.grid_columnconfigure(0, weight=1)
        screen_box.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(screen_box, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        result_box = tk.LabelFrame(
            middle,
            text="Kết quả chạy",
            font=("Arial", 12, "bold"),
            bg="white",
            height=240,
            padx=8,
            pady=8
        )
        result_box.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
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

        # Cot phai
        process_box = tk.LabelFrame(
            main,
            text="Quá trình các bước chạy",
            font=("Arial", 12, "bold"),
            bg="white",
            width=480,
            padx=8,
            pady=8
        )
        process_box.grid(row=0, column=2, sticky="nsew", padx=(16, 0))
        self.process_box = process_box
        process_box.grid_propagate(False)
        process_box.grid_columnconfigure(0, weight=1)
        process_box.grid_rowconfigure(0, weight=1)

        self.process_text = tk.Text(
            process_box,
            width=62,
            font=("Consolas", 10),
            wrap="none",
            state="disabled",
            bg="white"
        )
        self.process_text.grid(row=0, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(process_box, orient="vertical", command=self.process_text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.process_text.configure(yscrollcommand=yscroll.set)

    # ------------------------------------------------------------------
    # Man hinh khoi dau
    # ------------------------------------------------------------------

    def draw_start_screen(self):
        self.canvas.delete("all")
        self.set_result(
            "S =\n" + matrix_text(START_GRID, START_POS) +
            "\n\nG =\n" + matrix_text(GOAL_GRID)
        )
        start_node = Node("A", START_GRID, START_POS)
        self.draw_state(start_node, "Trạng thái bắt đầu", "Bấm nút bên trái để chạy thuật toán")

    def reset_app(self):
        self.switch_to_vacuum_view()
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        
        self.records = []
        self.display_records = []
        self.was_record_limited = False
        self.goal_node = None
        self.search_status = "failure"
        self.current_title = ""
        self.shown_frontier_names = set()
        
        self.process_text.config(state="normal")
        self.process_text.delete("1.0", "end")
        self.process_text.config(state="disabled")
        
        self.draw_start_screen()

    # ------------------------------------------------------------------
    # Cap nhat text
    # ------------------------------------------------------------------

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("end", text)
        self.result_text.config(state="disabled")

    def clear_process(self):
        self.shown_frontier_names = set()
        self.process_text.config(state="normal")
        self.process_text.delete("1.0", "end")
        
        if "Simulated Annealing" in self.current_title:
            self.process_text.insert(
                "end",
                f'{"T":<8}| {"Current (h)":<13}| {"Neighbor (h)":<13}| {"Delta":<6}| {"p / r":<15}| Quyết định\n' +
                "-" * 8 + "+-" + "-" * 13 + "+-" + "-" * 13 + "+-" + "-" * 6 + "+-" + "-" * 15 + "+-" + "-" * 15 + "\n"
            )
        elif "Local Beam Search" in self.current_title:
            self.process_text.insert(
                "end",
                "Quá trình tìm kiếm chùm (Local Beam Search):\n" +
                "-" * 65 + "\n"
            )
        elif "Hill" in self.current_title:
            self.process_text.insert(
                "end",
                f'{"Current":<10}| Neighbors\n' +
                "-" * 10 + "+-" + "-" * 70 + "\n"
            )
        elif "AND-OR" in self.current_title:
            self.process_text.insert(
                "end",
                f'{"Node":<8}| Chi tiết hoạt động đệ quy\n' +
                "-" * 8 + "+-" + "-" * 50 + "\n"
            )
        else:
            self.process_text.insert(
                "end",
                f'{"Node":<8}| {"Frontier":<42}| Reached\n' +
                "-" * 8 + "+-" + "-" * 42 + "+-" + "-" * 18 + "\n"
            )
        self.process_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Chay thuat toan
    # ------------------------------------------------------------------

    def run_algo(self, method, version=1):
        self.switch_to_vacuum_view()
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None

        if method in {"BFS", "DFS", "IDS"}:
            self.current_title = f"{method} cách {version}"
            self.goal_node, self.records, self.search_status = search(method, version=version)
        else:
            self.current_title = method
            self.goal_node, self.records, self.search_status = search(method)

        self.clear_process()
        self.set_result("Đang tính toán lời giải bằng " + self.current_title + "...")

        self.display_records = self.records[:MAX_SHOW_RECORDS]
        self.was_record_limited = len(self.records) > MAX_SHOW_RECORDS

        for record in self.display_records:
            self.add_process_row(record)

        if self.was_record_limited:
            self.process_text.config(state="normal")
            self.process_text.insert("end", f"\nChi hien thi {MAX_SHOW_RECORDS} buoc dau de tranh dung giao dien.\n")
            self.process_text.config(state="disabled")

        if self.current_title == "Random Restart Hill" and self.display_records:
            self.show_random_restart_step(0)
        elif self.goal_node is not None and isinstance(self.goal_node, Node):
            self.solution_path = path_to_root(self.goal_node)
            self.show_solution_step(0)
        else:
            self.show_final_result()

    def switch_to_vacuum_view(self):
        if self.map_coloring_frame is not None:
            self.map_coloring_frame.pause()
            self.map_coloring_frame.grid_remove()
        if self.belief_frame is not None:
            self.belief_frame.pause()
            self.belief_frame.grid_remove()
        self.middle_frame.grid()
        self.process_box.grid()

    def run_map_coloring(self, method):
        # Stop vacuum animations
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
            
        # Hide vacuum frames
        self.middle_frame.grid_remove()
        self.process_box.grid_remove()
        if self.belief_frame is not None:
            self.belief_frame.pause()
            self.belief_frame.grid_remove()
        
        # Show map coloring frame
        if self.map_coloring_frame is None:
            from gui.map_coloring_gui import MapColoringFrame
            self.map_coloring_frame = MapColoringFrame(self.main_frame, self.project_dir)
            
        self.map_coloring_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
        
        # Run CSP search
        goal_node, records, search_status = search(method)
        
        # Pass to map coloring frame
        self.map_coloring_frame.set_records(method, records)

    def run_belief(self, method):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
        self.middle_frame.grid_remove()
        self.process_box.grid_remove()
        if self.map_coloring_frame is not None:
            self.map_coloring_frame.pause()
            self.map_coloring_frame.grid_remove()
        if self.belief_frame is None:
            from gui.belief_gui import BeliefFrame
            self.belief_frame = BeliefFrame(self.main_frame)
        self.belief_frame.grid(row=0, column=1, columnspan=2, sticky="nsew")
        goal_node, records, search_status = search(method)
        self.belief_frame.set_records(method, records)

    # ------------------------------------------------------------------
    # Hien thi tung buoc qua trinh
    # ------------------------------------------------------------------

    def add_process_row(self, record):
        if record.get("reset_frontier_names"):
            self.shown_frontier_names = set()

        self.process_text.config(state="normal")
        if record.get("section"):
            self.process_text.insert("end", f"[{record['section']}]\n")
        
        if "Simulated Annealing" in self.current_title:
            T = record["T"]
            curr_str = f"{record['current_name']}(h={record['current_h']})"
            next_str = f"{record['next_name']}(h={record['next_h']})"
            delta = record["delta"]
            delta_str = f"{delta:+d}"
            
            if record["p"] is not None:
                p_r_str = f"{record['p']:.4f}/{record['r']:.4f}"
            else:
                p_r_str = "Delta < 0"
                
            decision = record["decision_note"]
            self.process_text.insert(
                "end",
                f"{T:<8.2f}| {curr_str:<13}| {next_str:<13}| {delta_str:<6}| {p_r_str:<15}| {decision}\n"
            )
            
        elif "Local Beam Search" in self.current_title:
            step = record["step"]
            beam_str = ", ".join(f"{name}(h={h})" for name, h in record["beam_states"])
            neighbors_str = ", ".join(f"{name}(h={h}) từ {parent}" for name, h, parent in record["neighbors"][:4])
            if len(record["neighbors"]) > 4:
                neighbors_str += "..."
            next_beam_str = ", ".join(f"{name}(h={h})" for name, h in record["next_beam"])
            
            self.process_text.insert(
                "end",
                f"[Bước {step}]\n"
                f" Beam: {{{beam_str}}}\n"
                f" Lân cận: [{neighbors_str}]\n"
                f" Chọn mới: {{{next_beam_str}}}\n\n"
            )
            
        elif "AND-OR" in self.current_title:
            node_label = record["node_label"]
            note = record["note"]
            self.process_text.insert(
                "end",
                f"{node_label:<8}| {note}\n"
            )
            
        else:
            frontier_lines = []
            for node in record["frontier"]:
                if node.name in self.shown_frontier_names and "A*" not in self.current_title:
                    frontier_lines.append(node.name)
                else:
                    parent_name = node.parent.name if node.parent else "-"
                    action_name = node.action if node.action else "-"

                    if "A*" in self.current_title:
                        f_value = node.cost + heuristic(node)
                        details = f"cost={node.cost}, h={heuristic(node)}, f={f_value}"
                    elif "Greedy" in self.current_title:
                        details = f"cost={node.cost}, h={heuristic(node)}"
                    elif "Hill" in self.current_title:
                        details = f"h={heuristic(node)}, v={-heuristic(node)}"
                    else:
                        details = f"cost={node.cost}"

                    line = f"{node.name}: [{matrix_short(node.grid, node.pos)}], {parent_name}, {action_name}, {details}"
                    frontier_lines.append(line)
                    self.shown_frontier_names.add(node.name)

            if not frontier_lines:
                frontier_lines = ["(rỗng)"]

            if "Hill" in self.current_title:
                for i, line in enumerate(frontier_lines):
                    current_label = record["node_label"] if i == 0 else ""
                    self.process_text.insert("end", f"{current_label:<10}| {line}\n")
            else:
                reached_text = "{" + ", ".join(record["reached"]) + "}" if record["reached"] else "{}"
                for i, line in enumerate(frontier_lines):
                    node_label = record["node_label"] if i == 0 else ""
                    reached = reached_text if i == 0 else ""
                    self.process_text.insert("end", f"{node_label:<8}| {line:<42}| {reached}\n")
            self.process_text.insert("end", "\n")
            
        self.process_text.see("end")
        self.process_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Ve luoi tren canvas
    # ------------------------------------------------------------------

    def draw_grid(self, x, y, cell, grid, pos, label):
        self.canvas.create_text(
            x + cell * (SIZE / 2.0), y - 18,
            text=label,
            font=("Arial", 13, "bold"),
            fill="#1e293b"
        )

        for r in range(SIZE):
            for c in range(SIZE):
                left = x + c * cell
                top = y + r * cell
                value = grid[r][c]

                if pos == (r, c):
                    fill = "#ffe4e6" if value == 1 else "#dbeafe"
                else:
                    fill = "#fef3c7" if value == 1 else "#f1f5f9"

                self.canvas.create_rectangle(
                    left, top, left + cell, top + cell,
                    fill=fill, outline="#64748b", width=2
                )

                if pos == (r, c):
                    cx = left + cell / 2
                    cy = top + cell / 2
                    robot_img = self.get_cached_image("robot", cell)
                    if robot_img:
                        self.canvas.create_image(cx, cy, image=robot_img, anchor="center")
                    else:
                        radius = cell * 0.34
                        self.canvas.create_oval(
                            cx - radius, cy - radius, cx + radius, cy + radius,
                            fill="#e0f2fe", outline="#0369a1", width=2
                        )
                        self.canvas.create_oval(
                            cx - radius * 0.35, cy - radius * 0.35,
                            cx + radius * 0.35, cy + radius * 0.35,
                            fill="#38bdf8", outline="#075985", width=1
                        )
                        self.canvas.create_oval(
                            cx - radius * 0.13, cy - radius * 0.13,
                            cx + radius * 0.13, cy + radius * 0.13,
                            fill="#0f172a", outline="#0f172a"
                        )
                        self.canvas.create_line(
                            cx + radius * 0.45, cy + radius * 0.45,
                            cx + radius * 0.82, cy + radius * 0.82,
                            fill="#0369a1", width=2
                        )
                elif value == 1:
                    cx = left + cell / 2
                    cy = top + cell / 2
                    stain_img = self.get_cached_image("stain", cell)
                    if stain_img:
                        self.canvas.create_image(cx, cy, image=stain_img, anchor="center")
                    else:
                        self.canvas.create_text(
                            cx,
                            cy,
                            text="👾",
                            font=("Segoe UI Emoji", int(cell * 0.45)),
                            fill="#111827"
                        )

    def draw_state(self, node, title, note):
        self.current_node = node
        self.current_state_title = title
        self.current_state_note = note

        self.canvas.delete("all")

        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w <= 1:
            canvas_w = 800
        if canvas_h <= 1:
            canvas_h = 500

        cell = int((canvas_h * 0.7) / SIZE)
        if cell < 50:
            cell = 50
        if cell > 80:
            cell = 80

        grid_w = cell * SIZE
        grid_h = cell * SIZE

        x = (canvas_w - grid_w) / 2
        y = (canvas_h - grid_h) / 2 + 15

        self.canvas.create_text(
            canvas_w / 2,
            35,
            text=title,
            font=("Arial", 18, "bold"),
            fill="#111827"
        )

        self.draw_grid(x, y, cell, node.grid, node.pos, node.name)

        if "A*" in self.current_title:
            f_value = node.cost + heuristic(node)
            stats_text = f"cost = {node.cost}, h = {heuristic(node)}, f = {f_value}"
        elif "Greedy" in self.current_title:
            stats_text = f"cost = {node.cost}, h = {heuristic(node)}"
        elif "Hill" in self.current_title:
            stats_text = f"h = {heuristic(node)}, v = {-heuristic(node)}"
        else:
            stats_text = f"cost = {node.cost}"

        self.canvas.create_text(
            canvas_w / 2,
            y + grid_h + 30,
            text=stats_text,
            font=("Arial", 12, "bold"),
            fill="#374151"
        )

    def on_canvas_configure(self, event):
        if self.current_node:
            self.draw_state(self.current_node, self.current_state_title, self.current_state_note)

    # ------------------------------------------------------------------
    # Hien thi ket qua
    # ------------------------------------------------------------------

    def show_solution_step(self, index):
        if index >= len(self.solution_path):
            self.show_final_result()
            return

        node = self.solution_path[index]
        action_text = f"Đi {node.action}" if node.action else "Bắt đầu"
        self.draw_state(
            node,
            f"{self.current_title} - Di chuyển bước {index}",
            f"Hành động: {action_text}"
        )
        self.after_id = self.after(STEP_DELAY, lambda: self.show_solution_step(index + 1))

    def show_random_restart_step(self, index):
        if index >= len(self.display_records):
            self.show_final_result()
            return

        record = self.display_records[index]
        section = record.get("section", "")
        title = f"{self.current_title} - bước {index + 1}"
        if section:
            title = section

        self.draw_state(record["show_node"], title, record["note"])
        self.after_id = self.after(STEP_DELAY, lambda: self.show_random_restart_step(index + 1))

    def show_final_result(self):
        self.after_id = None

        if self.goal_node is None:
            if self.search_status == "cutoff":
                self.set_result("Chưa tìm thấy lời giải trong giới hạn độ sâu đã chọn.")
            else:
                self.set_result("Không tìm thấy lời giải.")
            return

        path = path_to_root(self.goal_node)
        node_path = " -> ".join(node.name for node in path)
        action_path = " -> ".join(node.action for node in path[1:]) if len(path) > 1 else "(không có)"
        found_goal = self.search_status == "success" and is_goal(self.goal_node.grid)

        if found_goal:
            title = "Tìm thấy lời giải bằng " + self.current_title
            path_label = "Đường đi node: "
        else:
            title = "Không tìm thấy lời giải bằng " + self.current_title
            path_label = "Đường đi tốt nhất đã thử: "

        if "AND-OR" in self.current_title:
            from algorithms.and_or_graph_search import format_conditional_plan
            plan = getattr(self.goal_node, "plan", "failure")
            plan_str = "Kế hoạch điều kiện (Conditional Plan):\n" + format_conditional_plan(plan) + "\n"
        else:
            plan_str = ""

        result = (
            title + "\n"
            + path_label + node_path + "\n"
            + "Hành động: " + action_path + "\n"
            + "Tổng cost: " + str(self.goal_node.cost) + "\n\n"
            + plan_str
            + "Trạng thái cuối:\n" + matrix_text(self.goal_node.grid, self.goal_node.pos)
        )
        self.set_result(result)
