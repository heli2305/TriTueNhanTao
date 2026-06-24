# No Observation & Partially Observable - May Hut Bui 3x3
# No Observation:     biet grid, khong biet vi tri -> 9 trang thai ban dau
# Partial Observable: biet vi tri, quan sat o dang dung -> ~256 trang thai ban dau

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
    g[r][c] = 0  # hut o hien tai truoc khi di chuyen
    dr, dc = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}[action]
    nr = max(0, min(SIZE - 1, r + dr))
    nc = max(0, min(SIZE - 1, c + dc))
    return (nr, nc), tuple(tuple(row) for row in g)


def predict(belief, action):
    """Ap dung action len toan bo belief state -> belief moi."""
    next_belief = set()
    for pos, grid in belief:
        new_pos, new_grid = apply_action(pos, grid, action)
        next_belief.add((new_pos, new_grid))
    return frozenset(next_belief)


def observe(pos, grid):
    """Cam bien cuc bo: robot chi biet o dang dung sach hay ban."""
    r, c = pos
    return grid[r][c]


def update_belief(belief, obs):
    """Loc belief: chi giu cac trang thai phu hop voi quan sat."""
    return frozenset(
        (pos, grid) for pos, grid in belief
        if observe(pos, grid) == obs
    )


def is_goal(belief):
    """Dich dat duoc khi moi trang thai trong belief deu sach."""
    for _, grid in belief:
        for r in range(SIZE):
            for c in range(SIZE):
                if grid[r][c] == 1:
                    return False
    return True


def heuristic(belief):
    """Trung binh so o ban tren tat ca trang thai trong belief."""
    if not belief:
        return 0
    total = sum(grid[r][c] for _, grid in belief for r in range(SIZE) for c in range(SIZE))
    return total / len(belief)


def all_possible_grids():
    """Tao tat ca 2^9 = 512 grid 3x3 co the."""
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
        "log": f"Buoc 1: Khong biet vi tri. Belief = {len(initial)} trang thai\n\n"
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
                "log": f"=> DAT DICH!\nChuoi hanh dong: {' -> '.join(plan)}\n"
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
                    "log": f"Buoc {step}: '{action}' -> Belief: {len(nb)} trang thai, h={h}\n\n"
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

    obs_str = "Ban" if obs0 else "Sach"
    records.append({
        "belief": initial,
        "action": "-",
        "plan": [],
        "log": f"Buoc 1: Vi tri {BELIEF_POS}, obs={obs_str}. Belief = {len(initial)} trang thai\n\n"
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
                "log": f"=> DAT DICH!\nChuoi hanh dong: {' -> '.join(plan)}\n"
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
                    obs_str = "Ban" if obs else "Sach"
                    records.append({
                        "belief": nb,
                        "action": action,
                        "plan": plan + [action],
                        "log": f"Buoc {step}: '{action}', obs={obs_str} -> Belief: {len(nb)} trang thai, h={h}\n\n"
                    })
                    step += 1

    return None, records, "failure"
