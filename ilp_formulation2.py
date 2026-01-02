import pulp
from typing import List


def holding_cost(i: int, k: int, h: List[int]) -> int:
    if i == k:
        return 0
    return sum(h[i:k])


def solve_uls_ilp2(n: int, d: List[int], f: List[int], p: List[int], h: List[int]):
    model = pulp.LpProblem("ULS_ILP2_Z", pulp.LpMinimize)
    y = [pulp.LpVariable(f"y_{i + 1}", cat="Binary") for i in range(n)]
    z = {}
    for i in range(n):
        for k in range(i, n):
            z[(i, k)] = pulp.LpVariable(f"z_{i + 1}_{k + 1}", lowBound=0, cat="Continuous")

    model += (
            pulp.lpSum(f[i] * y[i] for i in range(n)) +
            pulp.lpSum(
                (p[i] + holding_cost(i, k, h)) * z[(i, k)]
                for i in range(n)
                for k in range(i, n)
            )
    )
    # Demand satisfaction
    for k in range(n):
        model += (
            pulp.lpSum(z[(i, k)] for i in range(k + 1)) == d[k],
            f"demand_{k+1}"
        )
    # Linking z, d and y
    for i in range(n):
        for k in range(i, n):
            model += (
                z[(i, k)] <= d[k] * y[i],
                f"link_{i + 1}_{k + 1}"
            )

    solver = pulp.CPLEX_CMD(msg=True)
    status = model.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        raise RuntimeError(f"Not optimal. Status: {pulp.LpStatus[status]}")

    obj = pulp.value(model.objective)
    y_values = [int(round(pulp.value(y[i]))) for i in range(n)]
    z_values = {(i + 1, k + 1): pulp.value(z[(i, k)]) for (i, k) in z}

    return obj, y_values, z_values
