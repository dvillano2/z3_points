from ortools.sat.python import cp_model
from structures import build_geometry
from utils import normal_directions
from tests import test_lines, test_planes, test_special_points


def milp_model(prime, m, threshold, seed=0):

    total_points = prime**3
    total_directions = prime**2 + prime + 1
    total_blocks = total_directions
    total_planes = total_directions * prime

    lines, planes = build_geometry(prime)
    normal_list = normal_directions(prime)
    test_lines(lines, prime)
    test_planes(planes, normal_list, prime)
    test_special_points(prime)

    model = cp_model.CpModel()

    # x[i] = 1 if point is in subset
    x = [model.NewBoolVar(f"x_{i}") for i in range(total_points)]

    # z_p[p] = 1 if plane p has exactly m points
    z_p = [model.NewBoolVar(f"plane_{p}_ok") for p in range(total_planes)]

    # b_b[block] = 1 if all planes in block are satisfied
    b_b = [model.NewBoolVar(f"block_{b}_ok") for b in range(total_blocks)]

    for i in [0, 1, prime, prime**2]:
        model.add(x[i] == 1)

    model.add(sum(x[i] for i in range(total_points)) == m * prime)

    line_bound = min(m, prime - m)
    for line in lines:
        model.Add(sum(x[i] for i in line) <= line_bound)

    for p, plane in enumerate(planes):
        s = sum(x[i] for i in plane)
        model.Add(s <= prime)

        # this is like an asymmetric M-linearization
        model.Add(s - m <= prime * (1 - z_p[p]))
        model.Add(s - m >= -m * (1 - z_p[p]))

    for b in range(total_blocks):
        block_plane_indices = list(range(b * prime, (b + 1) * prime))
        # if any zp is zero, so is bb
        for p_idx in block_plane_indices:
            model.Add(b_b[b] <= z_p[p_idx])

        # if all zp are one, so is b
        model.Add(
            b_b[b]
            >= sum(z_p[p_idx] for p_idx in block_plane_indices) - (prime - 1)
        )

    model.add(sum(b_b) >= threshold)

    solver = cp_model.CpSolver()
    solver.parameters.random_seed = seed
    solver.parameters.enumerate_all_solutions = False
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        points_selected = [
            i for i in range(total_points) if solver.Value(x[i]) == 1
        ]
        planes_ok = [
            p for p in range(total_planes) if solver.Value(z_p[p]) == 1
        ]
        blocks_ok = [
            b for b in range(total_blocks) if solver.Value(b_b[b]) == 1
        ]
        return solver, points_selected, planes_ok, blocks_ok
    print("No solution found")
    return None, None, None, None
