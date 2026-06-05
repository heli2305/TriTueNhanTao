# Package algorithms - export ham search() chung cho GUI

from algorithms.bfs_dfs import bfs_dfs_search
from algorithms.ucs import uniform_cost_search
from algorithms.ids import iterative_deepening_search
from algorithms.greedy import greedy_search
from algorithms.astar import a_star_search
from algorithms.idastar import ida_star_search
from algorithms.hill_climbing import (
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    random_restart_hill_climbing,
)
from algorithms.local_beam import local_beam_search
from algorithms.simulated_annealing import simulated_annealing


def search(method, version=1):
    """Ham dieu phoi chung: nhan ten thuat toan, tra ve (goal_node, records, status)."""
    if method == "UCS":
        return uniform_cost_search()

    if method == "Greedy":
        return greedy_search()

    if method == "A*":
        return a_star_search()

    if method == "IDS":
        return iterative_deepening_search(version=version)

    if method == "IDA*":
        return ida_star_search()

    if method == "Simple Hill Climbing":
        return simple_hill_climbing()

    if method == "Steepest Ascent Hill":
        return steepest_ascent_hill_climbing()

    if method == "Stochastic Hill":
        return stochastic_hill_climbing()

    if method == "Random Restart Hill":
        return random_restart_hill_climbing()

    if method == "Local Beam Search":
        return local_beam_search()

    if method == "Simulated Annealing":
        return simulated_annealing()

    # Mac dinh: BFS hoac DFS
    return bfs_dfs_search(method, version=version)
