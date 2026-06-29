# Package algorithms - export ham search() chung cho GUI

from algorithms.uninformed_search.bfs_dfs import bfs_dfs_search
from algorithms.uninformed_search.ucs import uniform_cost_search
from algorithms.uninformed_search.ids import iterative_deepening_search
from algorithms.informed_search.greedy import greedy_search
from algorithms.informed_search.astar import a_star_search
from algorithms.informed_search.idastar import ida_star_search
from algorithms.local_search.hill_climbing import (
    simple_hill_climbing,
    steepest_ascent_hill_climbing,
    stochastic_hill_climbing,
    random_restart_hill_climbing,
)
from algorithms.local_search.local_beam import local_beam_search
from algorithms.local_search.simulated_annealing import simulated_annealing
from algorithms.searching_in_complex_environment.and_or_graph_search import and_or_graph_search


def search(method, version=1):
    """Ham dieu phoi chung: nhan ten thuat toan, tra ve (goal_node, records, status)."""
    if method == "AND-OR Graph Search":
        return and_or_graph_search()

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

    if method == "Map Coloring - Backtracking":
        from algorithms.csp.backtracking import backtracking_search
        return backtracking_search()

    if method == "Map Coloring - Forward Checking":
        from algorithms.csp.forward_checking import forward_checking_search
        return forward_checking_search()

    if method == "Map Coloring - AC-3":
        from algorithms.csp.ac3 import ac3_search
        return ac3_search()

    if method == "Map Coloring - Min-Conflicts":
        from algorithms.csp.min_conflicts import min_conflicts_search
        return min_conflicts_search()

    if method == "No Observation":
        from algorithms.searching_in_complex_environment.belief_state_search import sensorless_greedy
        return sensorless_greedy()

    if method == "Partial Observation":
        from algorithms.searching_in_complex_environment.belief_state_search import partial_obs_greedy
        return partial_obs_greedy()

    # Mac dinh: BFS hoac DFS
    return bfs_dfs_search(method, version=version)
