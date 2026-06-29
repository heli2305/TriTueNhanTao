# Thuat toan AND-OR Graph Search

from node import Node, is_goal, state_key, valid_moves, make_child, next_name
from config import START_GRID, START_POS

def and_or_graph_search():
    start = Node("A", START_GRID, START_POS)
    records = []
    reached_names = []
    name_index = [1]  

    def get_next_name():
        name = next_name(name_index[0])
        name_index[0] += 1
        return name

    path = set()
    path_nodes = []
    
    memo = {}

    # OR_SEARCH(state, problem, path)
    def or_search(state, path, path_nodes):
        s_key = state_key(state)
        if s_key in path:
            records.append({
                "node_label": state.name,
                "show_node": state,
                "note": f"OR_SEARCH: Trạng thái {state.name} bị lặp trên đường đi (thất bại)"
            })
            return None, "failure"

        if s_key in memo:
            return memo[s_key]

        reached_names.append(state.name)

        records.append({
            "node_label": state.name,
            "show_node": state,
            "note": f"OR_SEARCH: Đang xét trạng thái {state.name}"
        })

        if is_goal(state.grid):
            records.append({
                "node_label": state.name,
                "show_node": state,
                "note": f"OR_SEARCH: {state.name} là trạng thái Đích!"
            })
            res = (state, [])
            memo[s_key] = res
            return res

        for move in valid_moves(state.pos):
            child_name = get_next_name()
            child = make_child(state, move, child_name)

            result_states = [child]

            path.add(s_key)
            path_nodes.append(state)

            plan = and_search(result_states, path, path_nodes)

            path_nodes.pop()
            path.remove(s_key)

            if plan != "failure":
                child_node, goal_node, child_plan = plan[child.name]
                res = (goal_node, [move[0], plan])
                memo[s_key] = res
                return res

        res = (None, "failure")
        memo[s_key] = res
        return res

    # AND_SEARCH(states, problem, path)
    def and_search(states, path, path_nodes):
        plans = {}
        for s in states:
            goal_node, plan_s = or_search(s, path, path_nodes)
            if plan_s == "failure":
                return "failure"
            plans[s.name] = (s, goal_node, plan_s)
        return plans

    goal_node, plan = or_search(start, path, path_nodes)

    if plan != "failure" and goal_node is not None:
        status = "success"
        goal_node.plan = plan
    else:
        status = "failure"
        goal_node = None

    return goal_node, records, status


def format_conditional_plan(plan, indent=""):
    if plan == []:
        return f"{indent}Đạt mục tiêu (Goal)\n"
    if plan == "failure":
        return f"{indent}Thất bại (Failure)\n"

    action, plans = plan
    res = f"{indent}Hành động: {action}\n"
    for state_name, (state, goal, sub_plan) in plans.items():
        res += f"{indent}Nếu ở trạng thái {state_name} (vị trí: {state.pos}):\n"
        res += format_conditional_plan(sub_plan, indent + "  ")
    return res
