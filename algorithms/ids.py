# Thuat toan IDS (Iterative Deepening Search)

from node import Node, is_goal, is_cycle, state_key, valid_moves, make_child, next_name, path_to_root
from config import START_GRID, START_POS, MAX_SEARCH_RECORDS, MAX_FRONTIER_SHOW, MAX_IDS_DEPTH


def depth_limited_search(limit, version=1, record_limit=MAX_SEARCH_RECORDS):
    start = Node("A", START_GRID, START_POS)
    frontier = [start]
    records = []
    expanded_names = []
    name_index = 1
    result = "failure"

    def short_frontier():
        return list(frontier[-MAX_FRONTIER_SHOW:])

    def reached_short():
        return list(expanded_names[-MAX_FRONTIER_SHOW:])

    def over_record_limit(node):
        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": short_frontier(),
            "reached": reached_short(),
            "note": "Dung IDS vi qua nhieu buoc, tranh treo giao dien"
        })
        return "search_cutoff", records

    if is_goal(start.grid):
        records.append({
            "node_label": "A",
            "show_node": start,
            "frontier": [],
            "reached": [],
            "note": "Trang thai dau da la G"
        })
        return start, records

    while frontier:
        node = frontier.pop()
        expanded_names.append(node.name)

        if len(records) >= record_limit:
            return over_record_limit(node)

        if version == 1 and is_goal(node.grid):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": "Tim thay G"
            })
            return node, records

        if node.cost >= limit:
            result = "cutoff"
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": f"Cham gioi han do sau {limit}"
            })
            continue

        if is_cycle(node):
            records.append({
                "node_label": node.name,
                "show_node": node,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": "Bo qua vi tao chu trinh"
            })
            continue

        found_child = None

        for move in reversed(valid_moves(node.pos)):
            child = make_child(node, move, next_name(name_index))
            name_index += 1

            if version == 2 and is_goal(child.grid):
                found_child = child
                break

            frontier.append(child)

        if found_child is not None:
            records.append({
                "node_label": f"{node.name} -> {found_child.name}",
                "show_node": found_child,
                "frontier": short_frontier(),
                "reached": reached_short(),
                "note": f"Tim thay {found_child.name} khi sinh tu {node.name}"
            })
            return found_child, records

        records.append({
            "node_label": node.name,
            "show_node": node,
            "frontier": short_frontier(),
            "reached": reached_short(),
            "note": "Da mo rong node"
        })

    return result, records


def _depth_limited_search_for_ids(limit, version=1):
    """Phien ban nhanh cua DLS chi dem nut, khong ghi record (dung noi bo cho IDS)."""
    frontier = [Node("A", START_GRID, START_POS)]
    name_index = 1
    expanded_count = 0

    while frontier:
        node = frontier.pop()
        expanded_count += 1

        if version == 1 and is_goal(node.grid):
            return node, expanded_count

        if node.cost >= limit:
            continue

        if is_cycle(node):
            continue

        for move in reversed(valid_moves(node.pos)):
            child = make_child(node, move, next_name(name_index))
            name_index += 1

            if version == 2 and is_goal(child.grid):
                return child, expanded_count

            frontier.append(child)

    return None, expanded_count


def iterative_deepening_search(version=1):
    all_records = []
    start = Node("A", START_GRID, START_POS)

    for depth in range(MAX_IDS_DEPTH + 1):
        result, expanded_count = _depth_limited_search_for_ids(depth, version=version)

        record = {
            "node_label": f"d={depth}",
            "show_node": start,
            "frontier": [],
            "reached": [f"{expanded_count} node"],
            "note": f"IDS cach {version}: da thu depth {depth}, mo rong {expanded_count} node"
        }
        record["reset_frontier_names"] = True
        record["section"] = f"IDS cach {version} - depth = {depth}"
        all_records.append(record)

        if isinstance(result, Node):
            path = path_to_root(result)
            path_names = []
            for node in path:
                path_names.append(node.name)
                all_records.append({
                    "node_label": node.name,
                    "show_node": node,
                    "frontier": [],
                    "reached": list(path_names),
                    "note": "Node nam tren duong di ket qua cua IDS"
                })
            return result, all_records, "success"

    return None, all_records, "cutoff"
