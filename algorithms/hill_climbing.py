# Cac thuat toan Hill Climbing

import random
from node import Node, is_goal, heuristic, valid_moves, make_child, next_name
from config import START_GRID, START_POS, MAX_RESTART


def simple_hill_climbing():
    start = Node("A", START_GRID, START_POS)
    records = []
    reached_names = [start.name]
    name_index = 1
    current = start

    def value_func(n):
        return -heuristic(n)

    while True:
        if is_goal(current.grid):
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": [],
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return current, records, "success"

        neighbors = []
        for move in valid_moves(current.pos):
            child = make_child(current, move, next_name(name_index))
            name_index += 1
            neighbors.append(child)

        found_better = False
        next_state = None
        for neighbor in neighbors:
            if value_func(neighbor) > value_func(current):
                next_state = neighbor
                found_better = True
                break

        records.append({
            "node_label": current.name,
            "show_node": current,
            "frontier": list(neighbors),
            "reached": list(reached_names),
            "note": f"Dang o node {current.name}, v = {value_func(current)}. " +
                    (f"Di den {next_state.name}" if found_better else "Ket thuc tai cuc dai cuc bo")
        })

        if found_better:
            reached_names.append(next_state.name)
            current = next_state
        else:
            return current, records, "failure"


def steepest_ascent_hill_climbing():
    start = Node("A", START_GRID, START_POS)
    records = []
    reached_names = [start.name]
    name_index = 1
    current = start

    def value_func(n):
        return -heuristic(n)

    while True:
        if is_goal(current.grid):
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": [],
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return current, records, "success"

        neighbors = []
        for move in valid_moves(current.pos):
            child = make_child(current, move, next_name(name_index))
            name_index += 1
            neighbors.append(child)

        if not neighbors:
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": [],
                "reached": list(reached_names),
                "note": "Khong co trang thai lan can"
            })
            return current, records, "failure"

        best_neighbor = max(neighbors, key=value_func)
        found_better = value_func(best_neighbor) > value_func(current)

        records.append({
            "node_label": current.name,
            "show_node": current,
            "frontier": list(neighbors),
            "reached": list(reached_names),
            "note": f"Dang o node {current.name}, v = {value_func(current)}. " +
                    (f"Di den Best_Neighbor {best_neighbor.name}" if found_better else "Ket thuc tai cuc dai cuc bo")
        })

        if found_better:
            reached_names.append(best_neighbor.name)
            current = best_neighbor
        else:
            return current, records, "failure"


def stochastic_hill_climbing():
    start = Node("A", START_GRID, START_POS)
    records = []
    reached_names = [start.name]
    name_index = 1
    current = start

    def value_func(n):
        return -heuristic(n)

    while True:
        if is_goal(current.grid):
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": [],
                "reached": list(reached_names),
                "note": "Tim thay G"
            })
            return current, records, "success"

        neighbors = []
        for move in valid_moves(current.pos):
            child = make_child(current, move, next_name(name_index))
            name_index += 1
            neighbors.append(child)

        better_neighbors = [n for n in neighbors if value_func(n) > value_func(current)]

        if not better_neighbors:
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": list(neighbors),
                "reached": list(reached_names),
                "note": f"Dang o node {current.name}, v = {value_func(current)}. Ket thuc tai cuc dai cuc bo (Better_Neighbors rong)"
            })
            return current, records, "failure"
        else:
            next_state = random.choice(better_neighbors)
            records.append({
                "node_label": current.name,
                "show_node": current,
                "frontier": list(neighbors),
                "reached": list(reached_names),
                "note": f"Dang o node {current.name}, v = {value_func(current)}. Chon ngau nhien {next_state.name} tu {len(better_neighbors)} node tot hon"
            })
            reached_names.append(next_state.name)
            current = next_state


def random_restart_hill_climbing():
    records = []
    name_index = 1
    best_node = None

    def value_func(n):
        return -heuristic(n)

    for restart in range(1, MAX_RESTART + 1):
        # Luot dau dung S, cac luot sau tao lai vi tri robot ngau nhien
        if restart == 1:
            current = Node("A", START_GRID, START_POS)
        else:
            random_pos = (random.randrange(len(START_GRID)), random.randrange(len(START_GRID[0])))
            current = Node(next_name(name_index), START_GRID, random_pos)
            name_index += 1

        reached_names = [current.name]
        first_record = True

        while True:
            if best_node is None or value_func(current) > value_func(best_node):
                best_node = current

            if is_goal(current.grid):
                record = {
                    "node_label": current.name,
                    "show_node": current,
                    "frontier": [],
                    "reached": list(reached_names),
                    "note": "Tim thay G"
                }
                if first_record:
                    record["section"] = f"Restart {restart}/{MAX_RESTART}"
                    record["reset_frontier_names"] = True
                records.append(record)
                return current, records, "success"

            neighbors = []
            for move in valid_moves(current.pos):
                child = make_child(current, move, next_name(name_index))
                name_index += 1
                neighbors.append(child)

            better_neighbors = [n for n in neighbors if value_func(n) > value_func(current)]

            if not better_neighbors:
                note = f"Dang o node {current.name}, v = {value_func(current)}. Better_Neighbors rong"
                if restart < MAX_RESTART:
                    note += ", chuyen sang restart tiep theo"
                else:
                    note += ", da het MAX_RESTART"

                record = {
                    "node_label": current.name,
                    "show_node": current,
                    "frontier": [],
                    "reached": list(reached_names),
                    "note": note
                }
                if first_record:
                    record["section"] = f"Restart {restart}/{MAX_RESTART}"
                    record["reset_frontier_names"] = True
                records.append(record)
                break

            next_state = max(better_neighbors, key=value_func)
            record = {
                "node_label": current.name,
                "show_node": current,
                "frontier": list(better_neighbors),
                "reached": list(reached_names),
                "note": f"Dang o node {current.name}, v = {value_func(current)}. Chon Best_Neighbor {next_state.name}"
            }
            if first_record:
                record["section"] = f"Restart {restart}/{MAX_RESTART}"
                record["reset_frontier_names"] = True
                first_record = False
            records.append(record)

            reached_names.append(next_state.name)
            current = next_state

    return best_node, records, "failure"
