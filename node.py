# Model du lieu Node va cac ham tien ich dung chung

from dataclasses import dataclass
from config import SIZE, START_GRID, START_POS


@dataclass
class Node:
    name: str
    grid: tuple
    pos: tuple
    parent: object = None
    action: str = ""
    cost: int = 0


# --- Kiem tra trang thai ---

def is_goal(grid):
    for row in grid:
        for cell in row:
            if cell != 0:
                return False
    return True


def is_cycle(node):
    current_key = state_key(node)
    parent = node.parent

    while parent is not None:
        if state_key(parent) == current_key:
            return True
        parent = parent.parent

    return False


# --- Khoa trang thai ---

def state_key(node):
    return (node.grid, node.pos)


# --- Heuristic ---

def heuristic(node):
    """Manhattan distance tu robot den o ban nhat gan nhat + so o ban."""
    dirty_cells = []

    for r in range(SIZE):
        for c in range(SIZE):
            if node.grid[r][c] == 1:
                dirty_cells.append((r, c))

    if not dirty_cells:
        return 0

    robot_r, robot_c = node.pos
    min_distance = SIZE * SIZE

    for dirty_r, dirty_c in dirty_cells:
        distance = abs(robot_r - dirty_r) + abs(robot_c - dirty_c)
        if distance < min_distance:
            min_distance = distance

    return len(dirty_cells) + min_distance


# --- Di chuyen ---

def valid_moves(pos):
    r, c = pos
    moves = []

    if r > 0:
        moves.append(("U", -1, 0))
    if r < SIZE - 1:
        moves.append(("D", 1, 0))
    if c > 0:
        moves.append(("L", 0, -1))
    if c < SIZE - 1:
        moves.append(("R", 0, 1))

    return moves


def make_child(node, move, name):
    action, dr, dc = move
    r, c = node.pos

    grid = [list(row) for row in node.grid]

    # Neu dang o o ban thi hut sach truoc khi di chuyen
    if grid[r][c] == 1:
        grid[r][c] = 0

    nr, nc = r + dr, c + dc
    new_grid = tuple(tuple(row) for row in grid)

    return Node(
        name=name,
        grid=new_grid,
        pos=(nr, nc),
        parent=node,
        action=action,
        cost=node.cost + 1
    )


# --- Tien ich ---

def next_name(i):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if i < len(letters):
        return letters[i]
    return letters[i % len(letters)] + str(i // len(letters))


def path_to_root(node):
    path = []
    while node is not None:
        path.append(node)
        node = node.parent
    path.reverse()
    return path


def matrix_text(grid, pos=None):
    lines = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            if pos == (r, c):
                row.append("x")
            else:
                row.append(str(grid[r][c]))
        lines.append(" ".join(row))
    return "\n".join(lines)


def matrix_short(grid, pos=None):
    rows = []
    for r in range(SIZE):
        row = []
        for c in range(SIZE):
            if pos == (r, c):
                row.append("x")
            else:
                row.append(str(grid[r][c]))
        rows.append("".join(row))
    return "/".join(rows)
