from typing import List
from utils import shift_point


def final_direction(prime: int) -> list[int]:
    return list(range(prime))


def final_line_translates(
    prime: int, line: List[int]
) -> List[List[List[int]]]:
    translates = [[[0] for _ in range(prime)] for _ in range(prime)]
    for y in range(prime):
        for z in range(prime):
            translates[z][y] = [
                shift_point(point, y * prime + z * prime**2, prime)
                for point in line
            ]
    return translates
