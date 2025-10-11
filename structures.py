from typing import List
from typing import Tuple
from itertools import product


def get_total_points(prime: int) -> int:
    return prime**3


def get_total_directions(prime: int) -> int:
    return sum([prime**2, prime, 1])


def expand_index(index: int, prime: int) -> Tuple[int, int, int]:
    z, xy = divmod(index, prime**2)
    y, x = divmod(xy, prime)
    return (x, y, z)


def shift_point(point: int, shift: int, prime: int) -> int:
    "returns point + int, all in index form"
    point_coords = expand_index(point, prime)
    shift_coords = expand_index(shift, prime)
    shifted_point = 0
    for i, (point_coord, shift_coord) in enumerate(
        zip(point_coords, shift_coords)
    ):
        shifted_point += ((point_coord + shift_coord) % prime) * (prime**i)
    return shifted_point


# Non flat lines


def non_flat_line_translates(
    prime: int, line: List[int]
) -> List[List[List[int]]]:
    "Line is assumed to be a line pointing outside of the x y plane"
    translates = [[[0] for _ in range(prime)] for _ in range(prime)]
    for x in range(prime):
        for y in range(prime):
            translates[y][x] = [
                shift_point(point, x + y * prime, prime) for point in line
            ]
    return translates


def non_flat_lines_through_origin(prime: int) -> List[List[List[int]]]:
    stereo_directions = [[[0] for _ in range(prime)] for _ in range(prime)]
    for x in range(prime):
        for y in range(prime):
            stereo_directions[y][x] = [
                ((t * x) % prime + ((t * y) % prime) * prime + t * prime**2)
                for t in range(prime)
            ]
    return stereo_directions


def all_non_flat_lines(prime: int) -> List[List[List[List[List[int]]]]]:
    origin_lines = non_flat_lines_through_origin(prime)
    spot_holder = [[[0] for _ in range(prime)] for _ in range(prime)]
    full_list = [[spot_holder for _ in range(prime)] for _ in range(prime)]
    for x, y, z, w in product(range(prime), repeat=4):
        full_list[y][x] = non_flat_line_translates(prime, origin_lines[w][z])
    return full_list


# Intermediate lines
def intermediate_lines_through_origin(prime: int) -> List[List[int]]:
    stereo_directions = [[0] for _ in range(prime)]
    for x in range(prime):
        stereo_directions[x] = [
            (t * x) % prime + t * prime for t in range(prime)
        ]
    return stereo_directions


def intermedaite_line_translates(
    prime: int, line: List[int]
) -> List[List[List[int]]]:
    "Line direction is 0 in z coord and nonzero in y coord"
    translates = [[[0] for _ in range(prime)] for _ in range(prime)]
    for x in range(prime):
        for z in range(prime):
            translates[z][x] = [
                shift_point(point, x + z * prime**2, prime) for point in line
            ]
    return translates


def all_intermediate_lines(prime: int) -> List[List[List[List[int]]]]:
    intermediate_lines = intermediate_lines_through_origin(prime)
    full_list = [
        [[0 for _ in range(prime)] for _ in range(prime)] for _ in range(prime)
    ]
    for x, z, w in product(range(prime), repeat=4):
        full_list[z][x] = intermedaite_line_translates(
            prime, intermediate_lines[w]
        )
    return full_list
