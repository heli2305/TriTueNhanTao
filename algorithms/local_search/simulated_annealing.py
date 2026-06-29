
import math
import random
from node import Node, is_goal, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS

def simulated_annealing(T0=100.0, Tmin=0.1, alpha=0.95):
    start = Node("A", START_GRID, START_POS)
    current = start
    T = T0
    records = []
    name_index = 1
    
    while T > Tmin:
        if is_goal(current.grid):
            records.append({
                "show_node": current,
                "T": T,
                "current_name": current.name,
                "current_h": heuristic(current),
                "next_name": current.name,
                "next_h": heuristic(current),
                "delta": 0,
                "accepted": True,
                "p": 1.0,
                "r": 0.0,
                "decision_note": "Tim thay G"
            })
            return current, records, "success"
            
        neighbors = []
        for move in valid_moves(current.pos):
            child = make_child(current, move, next_name(name_index))
            name_index += 1
            neighbors.append(child)
            
        if not neighbors:
            records.append({
                "show_node": current,
                "T": T,
                "current_name": current.name,
                "current_h": heuristic(current),
                "next_name": "-",
                "next_h": 0,
                "delta": 0,
                "accepted": False,
                "p": 0.0,
                "r": 0.0,
                "decision_note": "Khong co trang thai lan can"
            })
            return current, records, "failure"
            
        next_state = random.choice(neighbors)
        delta = heuristic(next_state) - heuristic(current)
        
        accepted = False
        note = ""
        p_val = None
        r_val = None
        
        if delta < 0:
            current = next_state
            accepted = True
            note = "Delta < 0"
        else:
            p_val = math.exp(-delta / T)
            r_val = random.random()
            if r_val < p_val:
                current = next_state
                accepted = True
                note = "Nhan (r < p)"
            else:
                note = "Tu choi"
                
        records.append({
            "show_node": current,
            "T": T,
            "current_name": current.parent.name if current.parent else start.name,
            "current_h": heuristic(current.parent) if current.parent else heuristic(start),
            "next_name": next_state.name,
            "next_h": heuristic(next_state),
            "delta": delta,
            "accepted": accepted,
            "p": p_val,
            "r": r_val,
            "decision_note": note
        })
        
        T = alpha * T
        
    return current, records, "failure"
