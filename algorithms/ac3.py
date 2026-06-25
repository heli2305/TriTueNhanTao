from algorithms.map_coloring import (
    VARIABLES,
    DOMAINS,
    ADJACENCY,
    format_assignment,
    format_domain
)

def ac3_search():
    records = []
    
    domains = {var: list(DOMAINS) for var in VARIABLES}
    domains["12"] = ["Đỏ"]
    domains["Go Vap"] = ["Xanh lá"]
    domains["Thu Duc"] = ["Vàng"]
    
    def get_assignment_from_domains(doms):
        return {var: doms[var][0] for var in VARIABLES if len(doms[var]) == 1}
    
    assignment = get_assignment_from_domains(domains)
    
    init_logs = [
        "Khởi tạo thuật toán AC-3:\n",
        "  + Thiết lập miền giá trị ban đầu:\n",
        f"    * D(12) = {format_domain(domains['12'])}\n",
        f"    * D(Go Vap) = {format_domain(domains['Go Vap'])}\n",
        f"    * D(Thu Duc) = {format_domain(domains['Thu Duc'])}\n",
        "    * Các quận khác có đầy đủ 4 màu.\n\n"
    ]
    
    queue = []
    for u in VARIABLES:
        for v in ADJACENCY[u]:
            queue.append((u, v))
            
    init_logs.append(f"Khởi tạo hàng đợi arcs (Tổng số: {len(queue)} cung):\n")
    queue_preview = ", ".join(f"({u}->{v})" for u, v in queue[:5])
    init_logs.append(f"  + Queue: [{queue_preview}, ...]\n\n")
    
    records.append({
        "assignment": dict(assignment),
        "domains": {k: list(v) for k, v in domains.items()},
        "active_arc": None,
        "log": "".join(init_logs)
    })
    
    step_num = 2
    
    def remove_inconsistent_values(Xi, Xj):
        removed = False
        for x in list(domains[Xi]):
            has_consistent_y = False
            for y in domains[Xj]:
                if x != y:
                    has_consistent_y = True
                    break
            if not has_consistent_y:
                domains[Xi].remove(x)
                removed = True
        return removed

    success = True
    while queue:
        Xi, Xj = queue.pop(0)
        log_step = f"Bước {step_num}:\n- Xét cung: {Xi} → {Xj}\n"
        
        if remove_inconsistent_values(Xi, Xj):
            removed_colors = [c for c in DOMAINS if c not in domains[Xi] and c in (records[-1]["domains"][Xi] if records else DOMAINS)]
            log_step += f"  => Phát hiện không nhất quán! Đã loại bỏ màu: {', '.join(removed_colors)} khỏi D({Xi})\n"
            log_step += f"  => Miền mới D({Xi}) = {format_domain(domains[Xi])}\n"
            
            if not domains[Xi]:
                log_step += f"  => LỖI: Miền giá trị D({Xi}) bị rỗng! Ràng buộc không khả thi.\n"
                success = False
                assignment = get_assignment_from_domains(domains)
                records.append({
                    "assignment": dict(assignment),
                    "domains": {k: list(v) for k, v in domains.items()},
                    "active_arc": (Xi, Xj),
                    "log": log_step + "\n"
                })
                break
                
            added_arcs = []
            for Xk in ADJACENCY[Xi]:
                if Xk != Xj:
                    arc = (Xk, Xi)
                    if arc not in queue:
                        queue.append(arc)
                        added_arcs.append(arc)
            
            if added_arcs:
                log_step += f"  => Thêm lại hàng đợi các cung ngược: {', '.join(f'({u}->{v})' for u, v in added_arcs)}\n"
        else:
            log_step += f"  => Miền giá trị nhất quán. Không có màu nào bị loại bỏ.\n"
            
        queue_preview = ", ".join(f"({u}->{v})" for u, v in queue[:4])
        log_step += f"  => Hàng đợi hiện tại (size={len(queue)}): [{queue_preview}"
        if len(queue) > 4:
            log_step += ", ..."
        log_step += "]\n\n"
        
        assignment = get_assignment_from_domains(domains)
        records.append({
            "assignment": dict(assignment),
            "domains": {k: list(v) for k, v in domains.items()},
            "active_arc": (Xi, Xj),
            "log": log_step
        })
        step_num += 1
        
    if success:
        unresolved = [var for var in VARIABLES if len(domains[var]) > 1]
        final_log = "=> Hoàn tất chạy thuật toán AC-3 thành công!\n"
        if unresolved:
            final_log += f"  * Các miền giá trị đã được nhất quán cung (Arc Consistent).\n"
            final_log += f"  * Tuy nhiên, một số quận vẫn còn nhiều màu khả dụng: {', '.join(f'D({v})={format_domain(domains[v])}' for v in unresolved[:3])}...\n"
        else:
            final_log += "  * Rất thú vị! Tất cả các quận đều đã được rút gọn về đúng duy nhất 1 màu.\n"
            
        records.append({
            "assignment": dict(assignment),
            "domains": {k: list(v) for k, v in domains.items()},
            "active_arc": None,
            "log": final_log
        })
    else:
        records.append({
            "assignment": dict(assignment),
            "domains": {k: list(v) for k, v in domains.items()},
            "active_arc": None,
            "log": "=> Thất bại! Đồ thị không khả thi để đạt tính nhất quán cung (Arc Consistency).\n"
        })
        
    return assignment, records, "success" if success else "failure"
