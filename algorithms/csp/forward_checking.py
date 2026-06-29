from algorithms.csp.map_coloring import (
    VARIABLES,
    DOMAINS,
    ADJACENCY,
    format_assignment,
    format_domain
)

def forward_checking_search():
    records = []
    assignment = {}
    domains = {var: list(DOMAINS) for var in VARIABLES}
    
    init_domain_str = ", ".join(f"D({k})={format_domain(v)}" for k, v in list(domains.items())[:4]) + ", ..."
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
        
        records.append({
            "assignment": dict(assignment),
            "domains": {k: list(v) for k, v in current_domains.items()},
            "log": f"Bước {step_num}:\n- Chọn {var}\n"
        })
        step_num += 1
        
        var_colors = list(current_domains[var])
        
        for color in var_colors:
            log_try = f"- Thử: {var} = {color}\n- Check: hợp lệ\n"
            new_domains = {k: list(v) for k, v in current_domains.items()}
            new_domains[var] = [color]
            
            fc_logs = []
            empty_domain = False
            failed_var = None
            
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
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in new_domains.items()},
                    "log": log_try + fc_text + f"=> Assignment = {format_assignment(assignment)}\n\n"
                })
                
                if solve(var_index + 1, new_domains):
                    return True
                    
                del assignment[var]
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in current_domains.items()},
                    "log": log_try + fc_text + f"- Nhánh con thất bại => Thử lại {var} khác {color} (Quay lui)\n"
                })
            else:
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in current_domains.items()},
                    "log": log_try + fc_text + f"  + Lỗi: D({failed_var}) bị rỗng => Không hợp lệ (Quay lui)\n"
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
