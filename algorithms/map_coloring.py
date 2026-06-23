#Backtracking va Forward Checking

SEEDS = {
    "12": (600, 200),
    "Go Vap": (600, 320),
    "Thu Duc": (950, 280),
    "9": (1250, 400),
    "2": (950, 550),
    "Binh Thanh": (800, 480),
    "Phu Nhuan": (680, 480),
    "Tan Binh": (560, 480),
    "Tan Phu": (440, 540),
    "Binh Tan": (320, 670),
    "11": (530, 660),
    "10": (610, 630),
    "3": (680, 580),
    "1": (760, 610),
    "4": (780, 690),
    "5": (650, 715),
    "6": (480, 740),
    "7": (880, 830),
    "8": (400, 940)
}

ADJACENCY = {
    "12": ["Binh Tan", "Tan Phu", "Tan Binh", "Go Vap", "Binh Thanh", "Thu Duc"],
    "Go Vap": ["12", "Tan Binh", "Phu Nhuan", "Binh Thanh"],
    "Thu Duc": ["12", "Binh Thanh", "2", "9"],
    "9": ["Thu Duc", "2"],
    "2": ["Thu Duc", "9", "Binh Thanh", "1", "4", "7"],
    "Binh Thanh": ["Go Vap", "12", "Thu Duc", "2", "Phu Nhuan", "1"],
    "Phu Nhuan": ["Go Vap", "Binh Thanh", "Tan Binh", "3", "1"],
    "Tan Binh": ["12", "Go Vap", "Phu Nhuan", "Tan Phu", "11", "10", "3"],
    "Tan Phu": ["12", "Tan Binh", "Binh Tan", "11", "6"],
    "Binh Tan": ["12", "Tan Phu", "6", "8"],
    "11": ["Tan Phu", "Tan Binh", "6", "10", "5"],
    "10": ["Tan Binh", "11", "3", "5"],
    "3": ["Tan Binh", "Phu Nhuan", "1", "10"],
    "1": ["Binh Thanh", "Phu Nhuan", "3", "5", "4", "2"],
    "4": ["1", "5", "2", "7", "8"],
    "5": ["10", "1", "11", "6", "8", "4"],
    "6": ["11", "Binh Tan", "Tan Phu", "5", "8"],
    "7": ["2", "4", "8"],
    "8": ["Binh Tan", "6", "5", "4", "7"]
}

VARIABLES = [
    "12", "Go Vap", "Thu Duc", "9", "2", "Binh Thanh", "Phu Nhuan",
    "Tan Binh", "Tan Phu", "Binh Tan", "11", "10", "3", "1", "4", "5", "6", "7", "8"
]

DOMAINS = ["Đỏ", "Xanh lá", "Vàng", "Xanh dương"]

def format_assignment(assignment):
    if not assignment:
        return "{}"
    return "{" + ", ".join(f"{k}={v}" for k, v in assignment.items()) + "}"

def format_domain(domain):
    if not domain:
        return "rỗng"
    return "{" + ", ".join(domain) + "}"


def backtracking_search():

    records = []
    assignment = {}
    
    # Buoc 1: Trang thai bat dau
    records.append({
        "assignment": dict(assignment),
        "log": "Bước 1: Assignment = {}\n\n"
    })
    
    step_num = 2
    
    def solve(var_index):
        nonlocal step_num
        if var_index == len(VARIABLES):
            return True
            
        var = VARIABLES[var_index]
        
        # Ghi nhan buoc chon bien
        log_header = f"Bước {step_num}:\n- Chọn {var}\n"
        records.append({
            "assignment": dict(assignment),
            "log": log_header
        })
        step_num += 1
        
        for color in DOMAINS:
            log_try = f"- Thử: {var} = {color}\n"
            
            # Kiem tra hop le voi cac lan can
            conflict = None
            for neighbor in ADJACENCY[var]:
                if neighbor in assignment and assignment[neighbor] == color:
                    conflict = neighbor
                    break
                    
            if conflict is None:
                assignment[var] = color
                log_valid = f"- Kiểm tra: hợp lệ\n=> Assignment = {format_assignment(assignment)}\n\n"
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + log_valid
                })
                
                if solve(var_index + 1):
                    return True
                    
                # Quay lui
                del assignment[var]
                log_backtrack = f"- Kiểm tra: hợp lệ nhưng nhánh con thất bại => Thử lại {var} khác {color} (Quay lui)\n"
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + log_backtrack
                })
            else:
                log_invalid = f"- Kiểm tra: {var} ≠ {conflict} => Không hợp lệ\n"
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + log_invalid
                })
                
        return False

    success = solve(0)
    
    if success:
        records.append({
            "assignment": dict(assignment),
            "log": f"=> Giải quyết thành công!\nAssignment cuối cùng: {format_assignment(assignment)}\n"
        })
    else:
        records.append({
            "assignment": dict(assignment),
            "log": "=> Thất bại! Không tìm được lời giải hợp lệ.\n"
        })
        
    return assignment, records, "success" if success else "failure"


def forward_checking_search():
    """Thuat toan quay lui ket hop kiem tra truoc (Forward Checking)."""
    records = []
    assignment = {}
    
    # Khoi tao mien gia tri (domains) cho tat ca cac bien
    domains = {var: list(DOMAINS) for var in VARIABLES}
    
    # Buoc 1: Khởi tạo
    init_domain_str = ", ".join(f"D({k})={format_domain(v)}" for k, v in domains.items()[:4]) + ", ..."
    records.append({
        "assignment": dict(assignment),
        "domains": {k: list(v) for k, v in domains.items()},
        "log": f"Bước 1: Assignment = {{}}, {init_domain_str}\n\n"
    })
    
    step_num = 2
    
    def solve(var_index, current_domains):
        nonlocal step_num
        if var_index == len(VARIABLES):
            return True
            
        var = VARIABLES[var_index]
        
        # Ghi nhan buoc chon bien
        log_header = f"Bước {step_num}:\n- Chọn {var}\n"
        records.append({
            "assignment": dict(assignment),
            "domains": {k: list(v) for k, v in current_domains.items()},
            "log": log_header
        })
        step_num += 1
        
        # Lay cac mau kha dung trong mien gia tri cua bien hien tai
        var_colors = list(current_domains[var])
        
        for color in var_colors:
            log_try = f"- Thử: {var} = {color}\n- Check: hợp lệ\n"
            
            # Sao chep mien gia tri de thuc hien cap nhat
            new_domains = {k: list(v) for k, v in current_domains.items()}
            new_domains[var] = [color]
            
            fc_logs = []
            empty_domain = False
            failed_var = None
            
            # Kiem tra truoc: loai bo mau nay khoi cac bien lan can chua gan mau
            for neighbor in ADJACENCY[var]:
                if neighbor not in assignment:
                    if color in new_domains[neighbor]:
                        new_domains[neighbor].remove(color)
                        fc_logs.append(f"  + D({neighbor}) = {format_domain(new_domains[neighbor])}")
                        if not new_domains[neighbor]:
                            empty_domain = True
                            failed_var = neighbor
            
            fc_text = "- Forward checking:\n" + "\n".join(fc_logs) + "\n" if fc_logs else "- Forward checking: không thay đổi miền lân cận\n"
            
            if not empty_domain:
                assignment[var] = color
                log_valid = fc_text + f"=> Assignment = {format_assignment(assignment)}\n\n"
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in new_domains.items()},
                    "log": log_try + log_valid
                })
                
                if solve(var_index + 1, new_domains):
                    return True
                    
                # Quay lui
                del assignment[var]
                log_backtrack = fc_text + f"- Nhánh con thất bại => Thử lại {var} khác {color} (Quay lui)\n"
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in current_domains.items()},
                    "log": log_try + log_backtrack
                })
            else:
                log_fail = fc_text + f"  + Lỗi: D({failed_var}) bị rỗng => Không hợp lệ (Quay lui)\n"
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in current_domains.items()},
                    "log": log_try + log_fail
                })
                
        return False

    success = solve(0, domains)
    
    if success:
        records.append({
            "assignment": dict(assignment),
            "domains": {var: [assignment[var]] for var in VARIABLES},
            "log": f"=> Giải quyết thành công!\nAssignment cuối cùng: {format_assignment(assignment)}\n"
        })
    else:
        records.append({
            "assignment": dict(assignment),
            "domains": {var: [] for var in VARIABLES},
            "log": "=> Thất bại! Không tìm được lời giải hợp lệ.\n"
        })
        
    return assignment, records, "success" if success else "failure"
