from typing import List
from utils import shift_point

def intermediate_lines_through_origin(prime: int) -> List[List[int]]:
    stereo_directions = [[0] for _ in range(prime)]
    for x in range(prime):
        stereo_directions[x] = [
            (t * x) % prime + t * prime for t in range(prime)
        ]
    return stereo_directions


def intermediate_line_translates(
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
    full_list: List[List[List[List[int]]]] = [[] for _ in range(prime)]
    for x in range(prime):
        full_list[x] = intermediate_line_translates(
            prime, intermediate_lines[x]
        )
    return full_list
