# uncapacitated-lot-sizing
Exact methods (ILP &amp; Dynamic Programming) for the Uncapacitated Lot Sizing Problem (ULS).

This repository contains exact solution methods for the
**Uncapacitated Lot Sizing Problem (ULS)**, a classical optimization problem
in production planning and scheduling.

The objective is to determine optimal production decisions over a finite
planning horizon in order to satisfy known demands at minimum total cost.

---

## Problem Description

The planning horizon is divided into `n` periods. For each period `t`, the
following parameters are given:

- `d_t`: demand
- `f_t`: fixed setup cost
- `p_t`: unit production cost
- `h_t`: unit holding cost

The initial inventory is assumed to be zero.

The goal is to decide **when** and **how much** to produce so as to minimize
the total production, setup, and inventory holding costs.

---

## Methods Implemented

The following exact approaches are implemented and compared:

- **ILP Formulation 1**: classical time-indexed integer linear programming model
- **ILP Formulation 2**: alternative compact ILP formulation
- **Dynamic Programming**: polynomial-time algorithm exploiting optimal substructure

---
