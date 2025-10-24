from structures import build_geometry
from z3 import Bool, Sum, If, And, Optimize, Int


PRIME = 5
TOTAL_POINTS = PRIME**3
TOTAL_DIRECTIONS = PRIME**2 + PRIME + 1
TOTAL_LINES = TOTAL_DIRECTIONS * PRIME**2
TOTAL_PLANES = TOTAL_DIRECTIONS * PRIME

lines, planes = build_geometry(PRIME)

# =============================


def make_points(prime):
    return [Bool(f"x_{i}") for i in range(prime**3)]


def line_sum(line, points):
    return Sum([If(points[index], 1, 0) for index in line])


def plane_sum(plane, line_sums):
    return Sum([line_sums[index] for index in plane])


def equidistribution(plane_sums, prime):
    return And([plane_sums[0] == plane_sums[i] for i in range(1, prime)])


# =============================


def build_model(prime):
    opt = Optimize()
    points = make_points(prime)
    # Basic constraints
    m = Int("m")
    size = m * prime
    for index in [0, 1, prime, prime**2]:
        opt.add(points[index])
    opt.add(m >= 2, m <= prime - 1)

    opt.add(
        Sum([If(points[index], 1, 0) for index in range(prime**3)]) == size
    )

    # Line constraints
    line_bound = If(m <= prime - m, m, prime - m)
    line_sums = []
    for line in lines:
        ls = line_sum(line, points)
        opt.add(ls <= line_bound)
        line_sums.append(ls)

    # Plane constraints
    plane_bound = prime
    plane_sums = []
    for plane in planes:
        ps = plane_sum(plane, line_sums)
        opt.add(ps <= plane_bound)
        plane_sums.append(ps)

    # Equidistribution
    equidistribution_flags = []
    total_planes = (prime**2 + prime + 1) * prime
    for index in range(0, total_planes, prime):
        equidistribution_flag = equidistribution(
            plane_sums[index : index + prime], prime
        )
        equidistribution_flags.append(equidistribution_flag)

    opt.maximize(Sum([If(flag, 1, 0) for flag in equidistribution_flags]))

    return opt, points, m
