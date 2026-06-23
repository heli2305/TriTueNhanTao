
import random
from node import Node, is_goal, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS

def local_beam_search(k=2):
    start = Node("A", START_GRID, START_POS)
    records = []
    name_index = 1
    
    current_states = [start]
    for _ in range(k - 1):
        curr = start
        for _ in range(random.randint(1, 3)):
            moves = valid_moves(curr.pos)
            if not moves:
                break
            curr = make_child(curr, random.choice(moves), next_name(name_index))
            name_index += 1
        current_states.append(curr)
        
    step_limit = 200
    for step in range(step_limit):
        neighbor_states = []
        for state in current_states:
            for move in valid_moves(state.pos):
                child = make_child(state, move, next_name(name_index))
                name_index += 1
                neighbor_states.append(child)
                
        if not neighbor_states:
            records.append({
                "show_node": current_states[0] if current_states else start,
                "step": step + 1,
                "beam_states": [(n.name, heuristic(n)) for n in current_states],
                "neighbors": [],
                "next_beam": []
            })
            return current_states[0] if current_states else start, records, "failure"
            
        for neighbor in neighbor_states:
            if is_goal(neighbor.grid):
                records.append({
                    "show_node": neighbor,
                    "step": step + 1,
                    "beam_states": [(n.name, heuristic(n)) for n in current_states],
                    "neighbors": [(n.name, heuristic(n), n.parent.name if n.parent else "-") for n in neighbor_states],
                    "next_beam": [(neighbor.name, heuristic(neighbor))]
                })
                return neighbor, records, "success"
                
        neighbor_states.sort(key=lambda n: heuristic(n))
        
        records.append({
            "show_node": current_states[0] if current_states else start,
            "step": step + 1,
            "beam_states": [(n.name, heuristic(n)) for n in current_states],
            "neighbors": [(n.name, heuristic(n), n.parent.name if n.parent else "-") for n in neighbor_states],
            "next_beam": [(n.name, heuristic(n)) for n in neighbor_states[:k]]
        })
        
        current_states = neighbor_states[:k]
        
    return current_states[0] if current_states else start, records, "failure"
