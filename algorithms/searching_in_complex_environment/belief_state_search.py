# No Observation & Partially Observable - Máy Hút Bụi 3x3
# No Observation:     biết grid, không biết vị trí -> 9 trạng thái ban đầu
# Partial Observable: biết vị trí, quan sát ô đang đứng -> ~256 trạng thái ban đầu

SIZE = 3
ACTIONS = ["U", "D", "L", "R"]

BELIEF_GRID = (
    (1, 0, 1),
    (0, 1, 0),
    (1, 0, 0),
)
BELIEF_POS = (0, 0)


def apply_action(pos, grid, action):
    r, c = pos
    g = [list(row) for row in grid]
    g[r][c] = 0  # hút ô hiện tại trước khi di chuyển
    dr, dc = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[action]
    nr = max(0, min(SIZE - 1, r + dr))
    nc = max(0, min(SIZE - 1, c + dc))
    return (nr, nc), tuple(tuple(row) for row in g)


def predict(belief, action):
    """Áp dụng action lên toàn bộ belief state -> belief mới."""
    next_belief = set()
    for pos, grid in belief:
        new_pos, new_grid = apply_action(pos, grid, action)
        next_belief.add((new_pos, new_grid))
    return frozenset(next_belief)


def observe(pos, grid):
    """Cảm biến cục bộ: robot chỉ biết ô đang đứng sạch hay bẩn."""
    r, c = pos
    return grid[r][c]


def update_belief(belief, obs):
    """Lọc belief: chỉ giữ các trạng thái phù hợp với quan sát."""
    return frozenset(
        (pos, grid) for pos, grid in belief
        if observe(pos, grid) == obs
    )


def is_goal(belief):
    """Đích đạt được khi mọi trạng thái trong belief đều sạch."""
    for _, grid in belief:
        for r in range(SIZE):
            for c in range(SIZE):
                if grid[r][c] == 1:
                    return False
    return True


def heuristic(belief):
    """Trung bình số ô bẩn trên tất cả trạng thái trong belief."""
    if not belief:
        return 0
    total = sum(grid[r][c] for _, grid in belief for r in range(SIZE) for c in range(SIZE))
    return total / len(belief)


def all_possible_grids():
    """Tạo tất cả 2^9 = 512 grid 3x3 có thể."""
    grids = []
    for mask in range(2 ** (SIZE * SIZE)):
        grid = tuple(
            tuple((mask >> (r * SIZE + c)) & 1 for c in range(SIZE))
            for r in range(SIZE)
        )
        grids.append(grid)
    return grids


def sensorless_greedy():
    initial = frozenset(((r, c), BELIEF_GRID) for r in range(SIZE) for c in range(SIZE))
    frontier = [(initial, [])]
    visited = {initial}
    records = []

    records.append({
        "belief": initial,
        "action": "-",
        "plan": [],
        "log": f"Bước 1: Không biết vị trí. Belief = {len(initial)} trạng thái\n\n"
    })

    step = 2
    while frontier:
        best_index = 0
        for i in range(1, len(frontier)):
            if heuristic(frontier[i][0]) < heuristic(frontier[best_index][0]):
                best_index = i
        belief, plan = frontier.pop(best_index)

        if is_goal(belief):
            records.append({
                "belief": belief,
                "action": "GOAL",
                "plan": plan,
                "log": f"=> ĐẠT ĐÍCH!\nChuỗi hành động: {' -> '.join(plan)}\n"
            })
            return plan, records, "success"

        for action in ACTIONS:
            nb = predict(belief, action)
            if nb not in visited:
                visited.add(nb)
                frontier.append((nb, plan + [action]))
                h = round(heuristic(nb), 1)
                records.append({
                    "belief": nb,
                    "action": action,
                    "plan": plan + [action],
                    "log": f"Bước {step}: '{action}' -> Belief: {len(nb)} trạng thái, h={h}\n\n"
                })
                step += 1

    return None, records, "failure"


def partial_obs_greedy():
    initial = frozenset((BELIEF_POS, g) for g in all_possible_grids())
    obs0 = observe(BELIEF_POS, BELIEF_GRID)
    initial = update_belief(initial, obs0)

    frontier = [(initial, [])]
    visited = {initial}
    records = []

    obs_str = "Bẩn" if obs0 else "Sạch"
    records.append({
        "belief": initial,
        "action": "-",
        "plan": [],
        "log": f"Bước 1: Vị trí {BELIEF_POS}, obs={obs_str}. Belief = {len(initial)} trạng thái\n\n"
    })

    step = 2
    while frontier:
        best_index = 0
        for i in range(1, len(frontier)):
            if heuristic(frontier[i][0]) < heuristic(frontier[best_index][0]):
                best_index = i
        belief, plan = frontier.pop(best_index)

        if is_goal(belief):
            records.append({
                "belief": belief,
                "action": "GOAL",
                "plan": plan,
                "log": f"=> ĐẠT ĐÍCH!\nChuỗi hành động: {' -> '.join(plan)}\n"
            })
            return plan, records, "success"

        for action in ACTIONS:
            predicted = predict(belief, action)
            possible_obs = {observe(pos, grid) for pos, grid in predicted}
            for obs in possible_obs:
                nb = update_belief(predicted, obs)
                if nb and nb not in visited:
                    visited.add(nb)
                    frontier.append((nb, plan + [action]))
                    h = round(heuristic(nb), 1)
                    obs_str = "Bẩn" if obs else "Sạch"
                    records.append({
                        "belief": nb,
                        "action": action,
                        "plan": plan + [action],
                        "log": f"Bước {step}: '{action}', obs={obs_str} -> Belief: {len(nb)} trạng thái, h={h}\n\n"
                    })
                    step += 1

    return None, records, "failure"
