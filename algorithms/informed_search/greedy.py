# Thuat toan Greedy Best-First Search

from node import Node, is_goal, state_key, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS


def greedy_search():
    start = Node("A", START_GRID, START_POS)
    frontier = [start]
    reached_keys = set()
    records = []
    reached_names = []
    name_index = 1

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
        best_index = 0
        for i in range(1, len(frontier)):
            if heuristic(frontier[i]) < heuristic(frontier[best_index]):
                best_index = i

        node = frontier.pop(best_index)
        reached_keys.add(state_key(node))
        reached_names.append(node.name)

        if is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": sorted(frontier, key=heuristic),
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return node, records, "success"

        for move in valid_moves(node.pos):
            child = make_child(node, move, next_name(name_index))
            child_key = state_key(child)

            in_frontier = False
            for item in frontier:
                if state_key(item) == child_key:
                    in_frontier = True
                    break

            if child_key in reached_keys or in_frontier:
                continue

            name_index += 1
            frontier.append(child)

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": sorted(frontier, key=heuristic),
            "reached": list(reached_names),
            "note": f"Da mo rong node, h = {heuristic(node)}"
        })

    return None, records, "failure"
