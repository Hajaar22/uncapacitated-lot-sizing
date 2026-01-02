import pulp
from typing import List


def solve_uls_ilp1(n: int, d: List[int], f: List[int], p: List[int], h: List[int], s0: int = 0):
    # Big-M
    m = [sum(d[t:]) for t in range(n)]

    # Model
    model = pulp.LpProblem("ULS_ILP1", pulp.LpMinimize)

    # Variables
    x = [pulp.LpVariable(f"x_{t + 1}", lowBound=0, cat="Continuous") for t in range(n)]
    s = [pulp.LpVariable(f"s_{t + 1}", lowBound=0, cat="Continuous") for t in range(n)]
    y = [pulp.LpVariable(f"y_{t + 1}", cat="Binary") for t in range(n)]

    # Objective
    model += (
        pulp.lpSum(f[t] * y[t] for t in range(n))
        + pulp.lpSum(p[t] * x[t] for t in range(n))
        + pulp.lpSum(h[t] * s[t] for t in range(n))
    )

    # Constraints
    for t in range(n):
        if t == 0:
            model += (s[t] == s0 + x[t] - d[t]), f"balance_{t + 1}"
        else:
            model += (s[t] == s[t - 1] + x[t] - d[t]), f"balance_{t + 1}"

        # Linking
        model += (x[t] <= m[t] * y[t]), f"link_{t + 1}"

    # Solve with CPLEX
    solver = pulp.CPLEX_CMD(msg=True)
    status = model.solve(solver)

    # Check status
    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"Not optimal. Status: {pulp.LpStatus[status]}")

    # Extract solution
    obj = pulp.value(model.objective)
    x_values = [pulp.value(v) for v in x]
    y_values = [int(round(pulp.value(v))) for v in y]
    s_values = [pulp.value(v) for v in s]

    return obj, x_values, y_values, s_values
