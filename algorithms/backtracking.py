from algorithms.map_coloring import (
    VARIABLES,
    DOMAINS,
    ADJACENCY,
    format_assignment
)

def backtracking_search():
    records = []
    assignment = {}
    
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
        
        records.append({
            "assignment": dict(assignment),
            "log": f"Bước {step_num}:\n- Chọn {var}\n"
        })
        step_num += 1
        
        for color in DOMAINS:
            log_try = f"- Thử: {var} = {color}\n"
            conflict = None
            for neighbor in ADJACENCY[var]:
                if neighbor in assignment and assignment[neighbor] == color:
                    conflict = neighbor
                    break
                    
            if conflict is None:
                assignment[var] = color
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + f"- Kiểm tra: hợp lệ\n=> Assignment = {format_assignment(assignment)}\n\n"
                })
                
                if solve(var_index + 1):
                    return True
                    
                del assignment[var]
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + f"- Kiểm tra: hợp lệ nhưng nhánh con thất bại => Thử lại {var} khác {color} (Quay lui)\n"
                })
            else:
                records.append({
                    "assignment": dict(assignment),
                    "log": log_try + f"- Kiểm tra: {var} ≠ {conflict} => Không hợp lệ\n"
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
