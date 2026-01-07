from typing import Tuple
from itertools import product


def get_total_points(prime: int) -> int:
    return prime**3


def get_total_directions(prime: int) -> int:
    return sum([prime**2, prime, 1])


def expand_index(index: int, prime: int) -> Tuple[int, int, int]:
    z, yx = divmod(index, prime**2)
    y, x = divmod(yx, prime)
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


def normal_directions(prime):
    final_list = []
    for z, x in product(range(prime), repeat=2):
        final_list.append((x, -1, z))
    for z in range(prime):
        final_list.append((1, 0, -z))
    final_list.append((0, 0, 1))
    return final_list
