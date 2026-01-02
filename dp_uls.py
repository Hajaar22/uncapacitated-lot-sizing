from typing import List, Tuple


def f0(n: int, d: List[int], f: List[int], p: List[int], h: List[int], s0: int = 0) \
        -> Tuple[float, List[int], List[int], List[int]]:

    prefix_d = [0] * (n + 1)
    for t in range(1, n + 1):
        prefix_d[t] = prefix_d[t - 1] + d[t - 1]

    def sum_d(k_from: int, t_to: int) -> int:
        """Sum of demand from period k_from to t_to (1-indexed, inclusive)."""
        return prefix_d[t_to] - prefix_d[k_from - 1]

    # Suffix sums of holding costs
    suffix_h = [0] * (n + 1)
    for t in range(n - 1, -1, -1):
        suffix_h[t] = suffix_h[t + 1] + h[t]

    # Modified production costs used ONLY in the DP recurrence
    p1 = [p[t] + suffix_h[t] for t in range(n)]

    # Constants used in the cost transformation
    h0 = sum(h)

    k1 = 0
    for t in range(1, n + 1):
        k1 -= h[t - 1] * prefix_d[t]
    # DP arrays
    g = [0.0] * (n + 1)
    kappa = [0] * (n + 1)     # kappa[t] = argmin k in {1..t}

    g[0] = h0 * s0 + k1
    # DP recurrence (bottom-up)
    for t in range(1, n + 1):
        best_val = float("inf")
        best_k = 1
        for k in range(1, t + 1):
            val = g[k - 1] + f[k - 1] + p1[k - 1] * sum_d(k, t)
            if val < best_val:
                best_val = val
                best_k = k
        g[t] = best_val
        kappa[t] = best_k
    # Reconstruct regeneration slots
    y = [0] * n
    regen: List[int] = []

    t = n
    while t > 0:
        k = kappa[t]
        regen.append(k)
        t = k - 1
    regen.reverse()

    for k in regen:
        y[k - 1] = 1
    # Build x (production)
    x = [0] * n
    for idx, k in enumerate(regen):
        end = (regen[idx + 1] - 1) if idx + 1 < len(regen) else n
        x[k - 1] = sum_d(k, end)
    # Simulate inventory s
    s = [0] * n
    inv = s0
    for t in range(1, n + 1):
        inv += x[t - 1] - d[t - 1]
        s[t - 1] = inv

    obj = 0.0
    for t in range(n):
        obj += f[t] * y[t] + p[t] * x[t] + h[t] * s[t]

    return obj, y, x, s
