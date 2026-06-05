# Thuat toan A* Search

from node import Node, is_goal, state_key, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS


def a_star_search():
    start = Node("A", START_GRID, START_POS)
    frontier = [start]
    reached = {}
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
        # Chon node co f = g + h nho nhat trong FRONTIER
        best_index = 0
        for i in range(1, len(frontier)):
            f_i = frontier[i].cost + heuristic(frontier[i])
            f_best = frontier[best_index].cost + heuristic(frontier[best_index])
            if f_i < f_best:
                best_index = i

        node = frontier.pop(best_index)

        if is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": sorted(frontier, key=lambda item: item.cost + heuristic(item)),
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return node, records, "success"

        # Dua node vua xet vao REACHED
        reached[state_key(node)] = node
        reached_names.append(node.name)

        for move in valid_moves(node.pos):
            child = make_child(node, move, next_name(name_index))
            child_key = state_key(child)
            old_reached = reached.get(child_key)

            # Neu da co trong REACHED ma duong moi khong tot hon thi bo qua
            if old_reached is not None:
                if child.cost >= old_reached.cost:
                    continue
                del reached[child_key]
                if old_reached.name in reached_names:
                    reached_names.remove(old_reached.name)

            # Neu da co trong FRONTIER thi chi cap nhat khi g moi nho hon
            frontier_index = -1
            for i in range(len(frontier)):
                if state_key(frontier[i]) == child_key:
                    frontier_index = i
                    break

            if frontier_index != -1:
                if child.cost < frontier[frontier_index].cost:
                    child.name = frontier[frontier_index].name
                    frontier[frontier_index] = child
                continue

            name_index += 1
            frontier.append(child)

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": sorted(frontier, key=lambda item: item.cost + heuristic(item)),
            "reached": list(reached_names),
            "note": f"Da mo rong node, f = {node.cost + heuristic(node)}"
        })

    return None, records, "failure"
