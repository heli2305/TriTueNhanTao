# Thuat toan BFS va DFS

from collections import deque
from node import Node, is_goal, state_key, valid_moves, make_child, next_name


def bfs_dfs_search(method, version=1):
    from config import START_GRID, START_POS
    start = Node("A", START_GRID, START_POS)
    records = []
    reached_keys = set()
    reached_names = []
    name_index = 1

    if method == "BFS":
        frontier = deque([start])
    else:
        frontier = [start]

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
        node = frontier.popleft() if method == "BFS" else frontier.pop()
        reached_keys.add(state_key(node))
        reached_names.append(node.name)

        if version == 1 and is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": list(frontier),
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return node, records, "success"

        found_child = None
        moves = valid_moves(node.pos)

        if method == "DFS":
            moves = list(reversed(moves))

        for move in moves:
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

            if version == 2 and is_goal(child.grid):
                found_child = child
                break

            frontier.append(child)

        if found_child is not None:
            records.append({
                "node_label": f"{node.name} -> {found_child.name}",
                "show_node": found_child,
                "frontier": list(frontier),
                "reached": list(reached_names),
                "note": f"Tim thay {found_child.name} khi sinh tu {node.name}"
            })
            return found_child, records, "success"

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": list(frontier),
            "reached": list(reached_names),
            "note": "Da mo rong node"
        })

    return None, records, "failure"
