from ortools.sat.python import cp_model
from structures import build_geometry  # your function to get lines and planes


def build_milp_model_with_bounds(prime, m, threshold):

    total_points = prime**3
    total_directions = prime**2 + prime + 1
    total_blocks = total_directions
    total_planes = total_directions * prime

    lines, planes = build_geometry(prime)

    model = cp_model.CpModel()

    # x[i] = 1 if point is in subset
    x = [model.NewBoolVar(f"x_{i}") for i in range(total_points)]

    if threshold > 0:
        # z_p[p] = 1 if plane p has exactly m points
        z_p = [model.NewBoolVar(f"plane_{p}_ok") for p in range(total_planes)]

        # b_b[block] = 1 if all planes in block are satisfied
        b_b = [model.NewBoolVar(f"block_{b}_ok") for b in range(total_blocks)]

    for i in [0, 1, prime, prime**2]:
        model.add(x[i] == 1)

    model.add(sum(x[i] for i in range(total_points)) == m * prime)

    # ----------------------
    # Plane equality constraints (z_p = 1 iff sum == m)
    # ----------------------

    for p, plane in enumerate(planes):
        s = sum(x[i] for i in plane)
        model.Add(s <= prime)

        if threshold > 0:
            # this is like an asymmetric M-linearization
            model.Add(s - m <= prime * (1 - z_p[p]))
            model.Add(s - m >= -m * (1 - z_p[p]))

    # ----------------------
    # Line bounds
    # ----------------------
    line_bound = min(m, prime - m)
    for line in lines:
        model.Add(sum(x[i] for i in line) <= line_bound)

    # ----------------------
    # Block constraints: b_b = AND(z_p for planes in block)
    # ----------------------
    if threshold > 0:
        for b in range(total_blocks):
            block_plane_indices = list(range(b * prime, (b + 1) * prime))
            # if any zp is zero, so is bb
            for p_idx in block_plane_indices:
                model.Add(b_b[b] <= z_p[p_idx])

            # if all zp are one, so is b
            model.Add(
                b_b[b]
                >= sum(z_p[p_idx] for p_idx in block_plane_indices)
                - (prime - 1)
            )

        model.add(sum(b_b) >= threshold)

    # ----------------------
    # Solve
    # ----------------------
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = False
    status = solver.Solve(model)

    if status == cp_model.FEASIBLE:
        print(f"Solution: total satisfied blocks = {solver.ObjectiveValue()}")
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
