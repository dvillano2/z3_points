from typing import List
from itertools import product
from utils import shift_point


def non_flat_line_translates(
    line: List[int], prime: int
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
    """something wrong here"""
    origin_lines = non_flat_lines_through_origin(prime)
    spot_holder = [[[0] for _ in range(prime)] for _ in range(prime)]
    full_list = [[spot_holder for _ in range(prime)] for _ in range(prime)]
    for x, y in product(range(prime), repeat=2):
        full_list[y][x] = non_flat_line_translates(origin_lines[y][x], prime)
    return full_list


def single_list_non_flat_lines(
    prime: int,
) -> List[List[int]]:
    final_length: int = prime**4
    place_holder: List[List[int]] = [[] for _ in range(final_length)]
    structured = all_non_flat_lines(prime)
    for x, y, z, w in product(range(prime), repeat=4):
        spot: int = prime**3 * x + prime**2 * y + prime * z + w
        place_holder[spot] = structured[x][y][z][w]
    return place_holder
