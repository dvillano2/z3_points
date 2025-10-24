from structures import build_geometry
from z3 import (
    Bool,
    Sum,
    If,
    And,
    Or,
    Optimize,
    Int,
    Solver,
    Implies,
    PbLe,
    PbEq,
    PbGe,
    sat,
)
from z3 import Tactic, set_param, Then


PRIME = 5
TOTAL_POINTS = PRIME**3
TOTAL_DIRECTIONS = PRIME**2 + PRIME + 1
TOTAL_LINES = TOTAL_DIRECTIONS * PRIME**2
TOTAL_PLANES = TOTAL_DIRECTIONS * PRIME


# =============================


def make_points(prime):
    return [Bool(f"x_{i}") for i in range(prime**3)]


def add_points(prime, m, solver):
    assert m <= prime - 1
    assert m >= 2
    points = make_points(prime)
    # Basic constraints
    for i, point in enumerate(points):
        if i in [0, 1, prime, prime**2]:
            solver.add(PbEq([(point, 1)], 1))

    size = m * prime

    solver.add(PbEq([(p, 1) for p in points], size))
    return points


def add_line_bounds(prime, opt, points, m, lines):
    line_bound = min(m, prime - m)
    for line in lines:
        opt.add(PbLe([(points[idx], 1) for idx in line], line_bound))
    return


def add_plane_bounds(prime, planes, opt, points):
    plane_bound = prime
    for plane in planes:
        opt.add(PbLe([(points[idx], 1) for idx in plane], plane_bound))
    return


def add_equidistribution(prime, points, planes, solver, threshold, m):
    """
    Flattened equidistribution check using integer sums.

    - Each plane: sum of points
    - Block counts as 1 if all planes in the block have exactly m points
    - Single top-level PbGe for threshold
    """
    total_planes = (prime**2 + prime + 1) * prime
    block_terms = []

    for block_start in range(0, total_planes, prime):
        block_planes = planes[block_start : block_start + prime]

        # Compute integer sum for each plane
        plane_sums = [
            Sum([If(points[i], 1, 0) for i in plane]) for plane in block_planes
        ]

        # Boolean: plane has exactly m points
        plane_ok = [plane_sum == m for plane_sum in plane_sums]

        # Block literal: all planes satisfied
        block_literal = Sum([If(flag, 1, 0) for flag in plane_ok]) == len(
            block_planes
        )

        # Add as top-level PB term with weight 1
        block_terms.append((block_literal, 1))

    # Single PbGe enforcing threshold
    solver.add(PbGe(block_terms, threshold))


# def add_equidistribution(prime, points, planes, solver, threshold, m):
#    total_planes = (prime**2 + prime + 1) * prime
#    block_terms = []
#
#    for block_start in range(0, total_planes, prime):
#        block_planes = planes[block_start : block_start + prime]
#
#        # Boolean per plane: plane has exactly m points
#        plane_flags = [
#            PbEq([(points[i], 1) for i in plane], m) for plane in block_planes
#        ]
#
#        # Boolean literal: True iff all planes in the block are OK
#        block_literal = PbEq([(pf, 1) for pf in plane_flags], len(plane_flags))
#
#        # Append to threshold terms
#        block_terms.append((block_literal, 1))
#
#    solver.add(PbGe(block_terms, threshold))


# first
# def add_equidistribution(prime, points, planes, opt, threshold, m):
#    total_planes = (prime**2 + prime + 1) * prime
#    block_terms = []
#
#    for block_start in range(0, total_planes, prime):
#        block_planes = planes[block_start : block_start + prime]
#        plane_flags = [
#            PbEq([(points[i], 1) for i in plane], m) for plane in block_planes
#        ]
#
#        block_terms.append(
#            (PbEq([(pf, 1) for pf in plane_flags], prime), 1)
#        )
#
#    opt.add(PbGe(block_terms, threshold))
#    return


def build_model(prime, m, threshold):
    set_param("sat.pb.solver", True)
    set_param("sat.local_search", True)
    set_param("sat.threads", 4)
    sol = Solver()
    sol.set("model", False)
    points = add_points(prime, m, sol)

    if sol.check() != sat:
        print(sol.statistics())
        print("Infeasble at make points stage")
        return None, None

    lines, planes = build_geometry(prime)

    add_line_bounds(prime, sol, points, m, lines)
    print("starting line bound check")
    if sol.check() != sat:
        print(sol.statistics())
        print("Infeasble at line bound stage")
        return None, None

    add_plane_bounds(prime, planes, sol, points)
    print("starting plane bound check")
    if sol.check() != sat:
        print(sol.statistics())
        print("Infeasble at plane bound stage")
        return None, None

    add_equidistribution(prime, points, planes, sol, threshold, m)
    print("starting equidistribution threshold check")
    if sol.check() != sat:
        print(sol.statistics())
        print("Infeasble at equidistribution threshold stage")
        return None, None

    print("got to the end")
    print(sol.statistics())
    return sol, points
