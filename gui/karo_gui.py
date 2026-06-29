import tkinter as tk
from tkinter import ttk
import time
import random

# Import cac thuat toan
from algorithms.adversarial_search.minimax import minimax_decision, check_winner
from algorithms.adversarial_search.alpha_beta import alpha_beta_decision
from algorithms.adversarial_search.expectimax import expectimax_decision

class KaroFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f2f4f7")
        
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.algorithm = "Minimax"
        self.game_mode = "Player vs AI (Bạn đi trước)"
        
        self.player_symbol = 'X'
        self.ai_symbol = 'O'
        self.current_turn = 'X' # X luon di truoc
        
        self.is_running = True
        self.hovered_cell = None
        self.after_id = None
        
        self.make_ui()
        self.reset_game()

    def make_ui(self):
        # Frame chia lam 2 cot: Trai (Banh co + control), Phai (Log qua trinh)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0, minsize=520)
        self.grid_rowconfigure(0, weight=1)
        
        # Vung ben trai
        left_container = tk.Frame(self, bg="#f2f4f7")
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left_container.grid_columnconfigure(0, weight=1)
        left_container.grid_rowconfigure(0, weight=0, minsize=50)  # Thong bao trang thai
        left_container.grid_rowconfigure(1, weight=5)              # Canvas ban co
        left_container.grid_rowconfigure(2, weight=0, minsize=140) # Panel dieu khien
        
        # Label thong bao luot choi / trang thai
        self.status_label = tk.Label(
            left_container,
            text="Chào mừng đến với Cờ Karo 3x3!",
            font=("Arial", 14, "bold"),
            bg="#f2f4f7",
            fg="#1e293b",
            pady=10
        )
        self.status_label.grid(row=0, column=0, sticky="ew")
        
        # LabelFrame chua Canvas
        canvas_box = tk.LabelFrame(
            left_container,
            text="Bàn cờ Karo 3x3",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )
        canvas_box.grid(row=1, column=0, sticky="nsew", pady=(0, 4))
        canvas_box.grid_columnconfigure(0, weight=1)
        canvas_box.grid_rowconfigure(0, weight=1)
        
        # Canvas ve ban co
        self.canvas = tk.Canvas(canvas_box, bg="white", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Leave>", self.on_mouse_leave)
        
        # Controls panel
        ctrl_panel = tk.LabelFrame(
            left_container,
            text="Cấu hình trò chơi",
            font=("Arial", 11, "bold"),
            bg="#f2f4f7",
            padx=10,
            pady=10
        )
        ctrl_panel.grid(row=2, column=0, sticky="ew", pady=4)
        
        # Lua chon che do choi
        tk.Label(ctrl_panel, text="Chế độ chơi:", font=("Arial", 10), bg="#f2f4f7").grid(row=0, column=0, sticky="w", pady=4)
        self.combo_mode = ttk.Combobox(
            ctrl_panel,
            values=[
                "Player vs AI (Bạn đi trước)",
                "AI vs Player (AI đi trước)",
                "Mô phỏng AI vs AI"
            ],
            state="readonly",
            width=26
        )
        self.combo_mode.set("Player vs AI (Bạn đi trước)")
        self.combo_mode.grid(row=0, column=1, sticky="w", padx=10, pady=4)
        self.combo_mode.bind("<<ComboboxSelected>>", self.on_config_change)
        
        # Nut reset game
        self.btn_reset = ttk.Button(ctrl_panel, text="Chơi lại (Reset)", command=self.reset_game)
        self.btn_reset.grid(row=0, column=2, sticky="e", padx=20, pady=4)
        
        # Thong tin thuat toan hien tai
        tk.Label(ctrl_panel, text="Thuật toán AI:", font=("Arial", 10), bg="#f2f4f7").grid(row=1, column=0, sticky="w", pady=4)
        self.algo_label = tk.Label(ctrl_panel, text="Minimax", font=("Arial", 10, "bold"), fg="#1d4ed8", bg="#f2f4f7")
        self.algo_label.grid(row=1, column=1, sticky="w", padx=10, pady=4)
 
        # Nut di tung buoc cho AI vs AI
        self.btn_step_ai = ttk.Button(ctrl_panel, text="AI đi tiếp", command=self.execute_ai_move, state="disabled")
        self.btn_step_ai.grid(row=1, column=2, sticky="e", padx=20, pady=4)
 
        # Cot ben phai: Ket qua tinh toan & Qua trinh tim kiem
        right_container = tk.LabelFrame(
            self,
            text="Quá trình AI tính toán nước đi",
            font=("Arial", 12, "bold"),
            bg="white",
            width=520,
            padx=10,
            pady=10
        )
        right_container.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        right_container.grid_propagate(False)
        right_container.grid_columnconfigure(0, weight=1)
        right_container.grid_rowconfigure(0, weight=1)
        
        self.process_text = tk.Text(
            right_container,
            font=("Consolas", 10),
            wrap="none",
            state="disabled",
            bg="white",
            relief="flat"
        )
        self.process_text.grid(row=0, column=0, sticky="nsew")
        
        yscroll = ttk.Scrollbar(right_container, orient="vertical", command=self.process_text.yview)
        yscroll.grid(row=0, column=1, sticky="ns")
        self.process_text.configure(yscrollcommand=yscroll.set)
        
        xscroll = ttk.Scrollbar(right_container, orient="horizontal", command=self.process_text.xview)
        xscroll.grid(row=1, column=0, sticky="ew")
        self.process_text.configure(xscrollcommand=xscroll.set)
 
    def set_algorithm(self, method):
        """Duoc goi boi app.py khi click chon nut ben trai"""
        self.algorithm = method
        self.algo_label.config(text=method)
        self.log_message(f"\n--- ĐÃ CHUYỂN SANG THUẬT TOÁN: {method.upper()} ---")
        
        # Neu game dang chay va den luot AI thi kich hoat luot AI tinh toan lai
        if self.is_running and self.is_ai_turn():
            self.trigger_ai_move()
 
    def on_config_change(self, event=None):
        self.game_mode = self.combo_mode.get()
        self.reset_game()
 
    def reset_game(self):
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
            
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.is_running = True
        self.hovered_cell = None
        
        # Thiet lap ky tu nguoi/AI va luot choi dua tren game_mode
        if self.game_mode == "Player vs AI (Bạn đi trước)":
            self.player_symbol = 'X'
            self.ai_symbol = 'O'
            self.current_turn = 'X'
            self.btn_step_ai.config(state="disabled")
            self.status_label.config(text="Đến lượt của bạn (X)", fg="#1e293b")
        elif self.game_mode == "AI vs Player (AI đi trước)":
            self.player_symbol = 'O'
            self.ai_symbol = 'X'
            self.current_turn = 'X'
            self.btn_step_ai.config(state="disabled")
            self.status_label.config(text="AI đang suy nghĩ...", fg="#475569")
            self.trigger_ai_move()
        else: # AI vs AI
            self.player_symbol = None
            self.ai_symbol = None
            self.current_turn = 'X'
            self.btn_step_ai.config(state="normal")
            self.status_label.config(text="Mô phỏng AI vs AI. Bấm 'AI đi tiếp' để chạy.", fg="#0f766e")
            
        self.clear_log()
        self.log_message("=== KHỞI TẠO VÁN CHƠI MỚI ===")
        self.log_message(f"Chế độ: {self.game_mode}")
        self.log_message(f"Thuật toán AI: {self.algorithm}")
        self.log_message("Trạng thái bàn cờ ban đầu: Trống")
        self.redraw_board()
 
    def is_ai_turn(self):
        if self.game_mode == "Player vs AI (Bạn đi trước)":
            return self.current_turn == self.ai_symbol
        elif self.game_mode == "AI vs Player (AI đi trước)":
            return self.current_turn == self.ai_symbol
        else: # AI vs AI
            # Trong che do AI vs AI, moi luot deu do AI thuc hien (chu dong qua nut bam hoac tu dong)
            return True
 
    def on_canvas_configure(self, event):
        self.redraw_board()
 
    def redraw_board(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1: w = 400
        if h <= 1: h = 400
        
        cell_w = w / 3
        cell_h = h / 3
        
        # Ve o dang hover (neu co)
        if self.is_running and self.hovered_cell is not None:
            r, c = self.hovered_cell
            if self.board[r][c] == ' ':
                x1, y1 = c * cell_w, r * cell_h
                x2, y2 = x1 + cell_w, y1 + cell_h
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#f1f5f9", outline="")
                
        # Ve cac duong luoi
        for i in range(1, 3):
            # Cac duong doc
            self.canvas.create_line(i * cell_w, 0, i * cell_w, h, fill="#cbd5e1", width=3)
            # Cac duong ngang
            self.canvas.create_line(0, i * cell_h, w, i * cell_h, fill="#cbd5e1", width=3)
            
        # Ve X va O
        pad_w = cell_w * 0.18
        pad_h = cell_h * 0.18
        
        for r in range(3):
            for c in range(3):
                symbol = self.board[r][c]
                x1 = c * cell_w + pad_w
                y1 = r * cell_h + pad_h
                x2 = (c + 1) * cell_w - pad_w
                y2 = (r + 1) * cell_h - pad_h
                
                if symbol == 'X':
                    # X: mau do san ho
                    self.canvas.create_line(x1, y1, x2, y2, fill="#ef4444", width=6, capstyle="round")
                    self.canvas.create_line(x2, y1, x1, y2, fill="#ef4444", width=6, capstyle="round")
                elif symbol == 'O':
                    # O: mau xanh bien
                    self.canvas.create_oval(x1, y1, x2, y2, outline="#3b82f6", width=6)
 
    def on_mouse_move(self, event):
        if not self.is_running or self.game_mode == "Mô phỏng AI vs AI":
            self.canvas.config(cursor="")
            return
            
        if self.current_turn != self.player_symbol:
            self.canvas.config(cursor="")
            return
            
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w <= 1 or h <= 1:
            return
            
        cell_w = w / 3
        cell_h = h / 3
        
        c = int(event.x / cell_w)
        r = int(event.y / cell_h)
        
        if 0 <= r < 3 and 0 <= c < 3:
            if self.board[r][c] == ' ':
                self.canvas.config(cursor="hand2")
                if self.hovered_cell != (r, c):
                    self.hovered_cell = (r, c)
                    self.redraw_board()
            else:
                self.canvas.config(cursor="")
                if self.hovered_cell is not None:
                    self.hovered_cell = None
                    self.redraw_board()
        else:
            self.canvas.config(cursor="")
            if self.hovered_cell is not None:
                self.hovered_cell = None
                self.redraw_board()
 
    def on_mouse_leave(self, event):
        if self.hovered_cell is not None:
            self.hovered_cell = None
            self.redraw_board()
 
    def on_canvas_click(self, event):
        if not self.is_running or self.game_mode == "Mô phỏng AI vs AI":
            return
            
        if self.current_turn != self.player_symbol:
            return
            
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cell_w = w / 3
        cell_h = h / 3
        
        c = int(event.x / cell_w)
        r = int(event.y / cell_h)
        
        if 0 <= r < 3 and 0 <= c < 3 and self.board[r][c] == ' ':
            self.hovered_cell = None
            self.make_move(r, c, self.player_symbol)
 
    def make_move(self, r, c, symbol):
        self.board[r][c] = symbol
        self.redraw_board()
        
        # Kiem tra ket thuc game
        winner = check_winner(self.board)
        if winner is not None:
            self.end_game(winner)
            return
            
        # Doi luot choi
        self.current_turn = 'O' if symbol == 'X' else 'X'
        
        if self.game_mode == "Mô phỏng AI vs AI":
            self.status_label.config(text=f"AI vs AI: Đến lượt quân {self.current_turn}", fg="#0f766e")
            self.btn_step_ai.config(state="normal")
        else:
            if self.current_turn == self.ai_symbol:
                self.status_label.config(text="AI đang suy nghĩ...", fg="#475569")
                self.trigger_ai_move()
            else:
                self.status_label.config(text=f"Đến lượt của bạn ({self.player_symbol})", fg="#1e293b")
 
    def trigger_ai_move(self):
        self.btn_step_ai.config(state="disabled")
        if self.after_id is not None:
            self.after_cancel(self.after_id)
        # Dung after de tao hieu ung tre giup UI muot ma
        self.after_id = self.after(400, self.execute_ai_move)
 
    def execute_ai_move(self):
        self.after_id = None
        if not self.is_running:
            return
            
        # AI thuc hien tinh toan
        symbol = self.current_turn
        
        self.log_message(f"\nAI ({symbol}) bắt đầu tính toán bằng {self.algorithm}...")
        
        start_time = time.perf_counter()
        
        # Goi thuat toan tuong ung
        if self.algorithm == "Minimax":
            best_move, best_score, nodes, move_scores = minimax_decision(self.board, symbol)
            pruned_text = ""
        elif self.algorithm == "Alpha-Beta":
            best_move, best_score, nodes, pruned, move_scores = alpha_beta_decision(self.board, symbol)
            pruned_text = f" | Số nhánh tỉa: {pruned}"
        else: # Expectimax
            best_move, best_score, nodes, move_scores = expectimax_decision(self.board, symbol)
            pruned_text = ""
            
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        
        if best_move is None:
            # Truong hop loi hoac ban co full (mac du da check_winner)
            self.log_message("LỖI: Không tìm thấy nước đi hợp lệ!")
            return
            
        r, c = best_move
        
        # Log ket qua chi tiet
        self.log_message(f"-> Nước đi tối ưu chọn: Hàng {r + 1}, Cột {c + 1} (Điểm đánh giá: {best_score})")
        self.log_message(f"-> Thống kê: Đã duyệt {nodes} node | Thời gian: {elapsed_ms:.2f} ms{pruned_text}")
        self.log_message("Chi tiết điểm số đánh giá các ô khả thi:")
        
        for move, score in move_scores:
            move_r, move_c = move
            self.log_message(f"   - Ô (Hàng {move_r + 1}, Cột {move_c + 1}): Điểm = {score}")
            
        # Thuc hien nuoc di
        self.make_move(r, c, symbol)
 
    def end_game(self, winner):
        self.is_running = False
        self.btn_step_ai.config(state="disabled")
        
        if winner == 'Tie':
            self.status_label.config(text="Kết quả: HÒA NHAU!", fg="#d97706")
            self.log_message("\n=== KẾT THÚC VÁN ĐẤU: HÒA NHAU ===")
        else:
            if self.game_mode == "Mô phỏng AI vs AI":
                self.status_label.config(text=f"Kết quả: AI {winner} THẮNG!", fg="#16a34a")
                self.log_message(f"\n=== KẾT THÚC VÁN ĐẤU: AI {winner} CHIẾN THẮNG! ===")
            else:
                if winner == self.player_symbol:
                    self.status_label.config(text="Chúc mừng! BẠN ĐÃ CHIẾN THẮNG!", fg="#16a34a")
                    self.log_message("\n=== KẾT THÚC VÁN ĐẤU: BẠN CHIẾN THẮNG AI! ===")
                else:
                    self.status_label.config(text="Rất tiếc! AI ĐÃ THẮNG BẠN!", fg="#dc2626")
                    self.log_message("\n=== KẾT THÚC VÁN ĐẤU: AI CHIẾN THẮNG BẠN! ===")
 
    # ------------------------------------------------------------------
    # CAC HAM PHU TRO LOG GIAO DIEN
    # ------------------------------------------------------------------
 
    def log_message(self, message):
        self.process_text.config(state="normal")
        self.process_text.insert("end", message + "\n")
        self.process_text.see("end")
        self.process_text.config(state="disabled")
 
    def clear_log(self):
        self.process_text.config(state="normal")
        self.process_text.delete("1.0", "end")
        self.process_text.config(state="disabled")
        
    def pause(self):
        """Khop voi phuong thuc dung hoat dong cua cac Frame khac"""
        if self.after_id is not None:
            self.after_cancel(self.after_id)
            self.after_id = None
