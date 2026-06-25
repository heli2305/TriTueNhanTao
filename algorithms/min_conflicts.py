import random
from algorithms.map_coloring import VARIABLES, DOMAINS, ADJACENCY, format_assignment

def get_conflicts(var, val, assignment):
    count = 0
    for neighbor in ADJACENCY[var]:
        if assignment.get(neighbor) == val:
            count += 1
    return count

def get_conflicted_vars(assignment):
    conflicted = []
    for var in VARIABLES:
        if get_conflicts(var, assignment[var], assignment) > 0:
            conflicted.append(var)
    return conflicted

def min_conflicts_search(max_steps=500):
    records = []
    
    random.seed(42)
    current = {var: random.choice(DOMAINS) for var in VARIABLES}
    
    records.append({
        "assignment": dict(current),
        "active_var": None,
        "log": f"Khởi tạo trạng thái ngẫu nhiên:\n  Assignment = {format_assignment(current)}\n\n"
    })
    
    step_num = 2
    success = False
    
    for step in range(1, max_steps + 1):
        conflicted_vars = get_conflicted_vars(current)
        
        if not conflicted_vars:
            success = True
            break
            
        var = random.choice(conflicted_vars)
        old_color = current[var]
        
        min_c = get_conflicts(var, old_color, current)
        best_candidates = [old_color]
        
        for val in DOMAINS:
            if val != old_color:
                c = get_conflicts(var, val, current)
                if c < min_c:
                    min_c = c
                    best_candidates = [val]
                elif c == min_c:
                    best_candidates.append(val)
                    
        best_val = random.choice(best_candidates)
        current[var] = best_val
        
        log_step = (
            f"Bước {step_num}:\n"
            f"- Quận bị xung đột được chọn: {var} (màu cũ: {old_color})\n"
            f"- Đổi màu thành: {best_val} (xung đột tối thiểu: {min_c})\n"
            f"- Assignment = {format_assignment(current)}\n\n"
        )
        
        records.append({
            "assignment": dict(current),
            "active_var": var,
            "log": log_step
        })
        step_num += 1
        
    if success:
        records.append({
            "assignment": dict(current),
            "active_var": None,
            "log": f"=> Giải quyết thành công!\nAssignment cuối cùng: {format_assignment(current)}\n"
        })
    else:
        records.append({
            "assignment": dict(current),
            "active_var": None,
            "log": "=> Thất bại! Vượt quá số bước lặp tối đa.\n"
        })
        
    return current, records, "success" if success else "failure"
