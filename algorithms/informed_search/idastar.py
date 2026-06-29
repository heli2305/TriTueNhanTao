# Thuat toan IDA* (Iterative Deepening A*)

from node import Node, is_goal, is_cycle, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS, MAX_SEARCH_RECORDS, MAX_FRONTIER_SHOW


def f_limited_search(f_limit, record_limit):
    start = Node("A", START_GRID, START_POS)
    frontier = [start]
    records = []
    expanded_names = []
    name_index = 1
    next_limit = float("inf")

    def short_frontier():
        return list(frontier[-MAX_FRONTIER_SHOW:])

    def reached_short():
        return list(expanded_names[-MAX_FRONTIER_SHOW:])

    def over_record_limit(node, note):
        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": short_frontier(),
            "reached": reached_short(),
            "note": note
        })
        return "cutoff", records, next_limit

    if is_goal(start.grid):
        records.append({
            "node_label": "A",
            "show_node": start,
            "frontier": [],
            "reached": [],
            "note": "Trang thai dau da la G"
        })
        return start, records, next_limit

    while frontier:
        node = frontier.pop()
        expanded_names.append(node.name)

        if len(records) >= record_limit:
            return over_record_limit(node, "Dung IDA* vi qua nhieu buoc, tranh treo giao dien")

        f_value = node.cost + heuristic(node)

        if f_value > f_limit:
            next_limit = min(next_limit, f_value)
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": f"Vuot gioi han f: f = {f_value} > {f_limit}"
            })
            continue

        if is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": "Tim thay G"
            })
            return node, records, next_limit

        if is_cycle(node):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": "Bo qua vi tao chu trinh"
            })
            continue

        for move in reversed(valid_moves(node.pos)):
            child = make_child(node, move, next_name(name_index))
            name_index += 1
            frontier.append(child)

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": short_frontier(),
            "reached": reached_short(),
            "note": f"Da mo rong node, f = {f_value}"
        })

    return None, records, next_limit


def ida_star_search():
    start = Node("A", START_GRID, START_POS)
    f_limit = start.cost + heuristic(start)
    all_records = []

    while f_limit != float("inf"):
        remaining_records = MAX_SEARCH_RECORDS - len(all_records)
        if remaining_records <= 0:
            return None, all_records, "cutoff"

        result, records, next_limit = f_limited_search(f_limit, remaining_records)

        if records:
            records[0]["reset_frontier_names"] = True
            records[0]["section"] = f"IDA* - f_limit = {f_limit}"
            all_records.extend(records)

        if isinstance(result, Node):
            return result, all_records, "success"

        if result == "cutoff":
            return None, all_records, "cutoff"

        if next_limit == float("inf"):
            break

        f_limit = next_limit

    return None, all_records, "failure"
