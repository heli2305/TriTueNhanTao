# Thuat toan Uniform Cost Search (UCS)

import heapq
from node import Node, is_goal, state_key, valid_moves, make_child, next_name


def uniform_cost_search():
    from config import START_GRID, START_POS
    start = Node("A", START_GRID, START_POS)
    frontier = [(start.cost, 0, start)]
    best_costs = {state_key(start): start.cost}
    records = []
    reached_names = []
    name_index = 1
    push_index = 1

    if is_goal(start.grid):
        records.append({
            "node_label": "A",
            "show_node": start,
            "frontier": [],
            "reached": [],
            "note": "Trang thai dau da la G"
        })
        return start, records, "success"

    while frontier:
        _, _, node = heapq.heappop(frontier)
        node_key = state_key(node)

        if node.cost > best_costs.get(node_key, float("inf")):
            continue

        reached_names.append(node.name)

        if is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": [item[2] for item in sorted(frontier)],
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return node, records, "success"

        for move in valid_moves(node.pos):
            child = make_child(node, move, next_name(name_index))
            name_index += 1
            child_key = state_key(child)

            if child.cost < best_costs.get(child_key, float("inf")):
                best_costs[child_key] = child.cost
                heapq.heappush(frontier, (child.cost, push_index, child))
                push_index += 1

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": [item[2] for item in sorted(frontier)],
            "reached": list(reached_names),
            "note": "Da mo rong node"
        })

    return None, records, "failure"
