# Cau hinh bai toan May Hut Bui

SIZE = 5

START_GRID = (
    (0, 0, 0, 0, 0),
    (0, 1, 1, 0, 0),
    (0, 0, 0, 1, 0),
    (0, 1, 0, 0, 0),
    (0, 0, 0, 1, 1),
)

START_POS = (0, 0)

GOAL_GRID = (
    (0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0),
)

# Gioi han cac tham so tim kiem
MAX_RESTART = 5
MAX_SHOW_RECORDS = 300
MAX_SEARCH_RECORDS = 10000
MAX_FRONTIER_SHOW = 60
MAX_IDS_DEPTH = 30

# Do tre hien thi (ms)
STEP_DELAY = 250
