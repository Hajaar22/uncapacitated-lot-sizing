# Uncapacitated Lot Sizing Problem (ULS)

This repository contains exact solution methods for the
**Uncapacitated Lot Sizing Problem (ULS)**, a classical optimization problem
in production planning and scheduling.

The objective is to determine optimal production decisions over a finite
planning horizon in order to satisfy known demands at minimum total cost.

---

## Problem Description

The planning horizon is divided into `n` periods (t = 1, …, n).  
For each period `t`, the following parameters are given:

- d(t): demand
- f(t): fixed setup cost
- p(t): unit production cost
- h(t): unit holding cost

The initial inventory is assumed to be zero.

The goal is to decide **when** and **how much** to produce so as to minimize
the total production, setup, and inventory holding costs.

---

## Mathematical Formulations

### ILP Formulation 1 (Time-Indexed Formulation)

#### Decision Variables
- x(t) ≥ 0 : quantity produced in period t  
- s(t) ≥ 0 : inventory level at the end of period t  
- y(t) ∈ {0,1} : equals 1 if production occurs in period t  

#### Objective Function
Minimize the total cost:

∑ₜ [ f(t) · y(t) + p(t) · x(t) + h(t) · s(t) ]

#### Constraints
- Inventory balance:  
  s(t−1) + x(t) − d(t) = s(t), for all t  

- Setup–production linking:  
  x(t) ≤ M · y(t), for all t  

- Variable domains:  
  x(t), s(t) ≥ 0 ; y(t) ∈ {0,1}

---

### ILP Formulation 2 (Aggregated Production Formulation)

This formulation explicitly assigns production in one period to demands in
future periods.

#### Decision Variables
- x(t,k) ≥ 0 : quantity produced in period t to satisfy demand in period k,
  with k ≥ t  
- y(t) ∈ {0,1} : setup decision in period t  

#### Objective Function
Minimize the total cost:

∑ₜ [ f(t) · y(t) ]  
+ ∑ₜ ∑ₖ≥ₜ [ ( p(t) + holding_cost(t,k) ) · x(t,k) ]

where `holding_cost(t,k)` is the cumulative inventory cost incurred when
producing in period t to satisfy demand in period k.

#### Constraints
- Demand satisfaction:  
  ∑ₜ≤ₖ x(t,k) = d(k), for all k  

- Setup–production linking:  
  ∑ₖ≥ₜ x(t,k) ≤ M · y(t), for all t  

- Variable domains:  
  x(t,k) ≥ 0 ; y(t) ∈ {0,1}

---

### Dynamic Programming Formulation

Let F(t) denote the minimum cost required to satisfy demands from period t
to period n.

At period t, production may occur to cover demands up to some future
period k ≥ t.

The recurrence relation is:

F(t) = min over k ≥ t of the following total cost:
- setup cost incurred in period t: f(t)
- production cost for demands d(t) to d(k) produced in period t
- inventory holding cost for storing units until period k
- optimal cost for the remaining periods: F(k+1)

The boundary condition is:
- F(n+1) = 0

This formulation exploits the optimal substructure of the Uncapacitated Lot
Sizing Problem and can be solved in polynomial time.

---
