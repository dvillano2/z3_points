"""
usage at non flat stage:
line_list, translator = single_list_non_flat_lines(prime)
non_indexed = all_non_flat_plane_groupings(5)
indexed = all_non_flat_plane_groupings_index(non_indexed, translator)

line_list will be a list of all lines (list of lists)
indexed will be a list of lists where each element represents a
line via its spot in line_list

so for the program, you can sum over everything in the line list
(zeros, ones) demand that they're below the bound, then sum each
of those via the plane groupings and demand they're under p + 1
and the score bumps up if you get the same answer fo
every chunk of the form [kp:(k+1)p]
"""

from typing import List
from typing import Dict
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


# Non flat lines


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


def lines_for_plane_organization(prime: int) -> List[List[List[int]]]:
    """
    Give a plane of points, give a list of all lines
    in the plane ordered so that every [a*prime : (a+1)*prime}]
    form a chunk of parallel lines. Useful for plane gorupings
    """
    x_function_lines = [
        [
            [[x, ((m * x) + b) % prime] for x in range(prime)]
            for b in range(prime)
        ]
        for m in range(prime)
    ]
    vertical_lines = [[[b, y] for y in range(prime)] for b in range(prime)]
    final_list = [[] for _ in range(prime**2 + prime)]
    for a in range(prime):
        for b in range(prime):
            final_list[a + prime * b] = x_function_lines[b][a]
    for a in range(prime):
        final_list[prime**2 + a] = vertical_lines[a]
    return final_list


def planes_from_line(non_flat_direction, prime):
    """
    returns a list of lists such that each
    sub list is list of lines in the given
    direction that comprise a plane
    moreover, each slice of the for [a*prime: (a+1)*prime]
    comprise a plane
    all such planes are given this way
    """
    translates = non_flat_line_translates(non_flat_direction, prime)
    indices = lines_for_plane_organization(prime)
    in_place = indices
    for a, _ in enumerate(in_place):
        for b, __ in enumerate(in_place[0]):
            in_place[a][b] = translates[in_place[a][b][0]][in_place[a][b][1]]
    return in_place


def all_non_flat_plane_groupings(prime: int):
    through_origin = non_flat_lines_through_origin(prime)
    place_holder = []
    for directions in through_origin:
        for direction in directions:
            place_holder.extend(planes_from_line(direction, prime))
    return place_holder


def planes_from_line_index_version(non_flat_direction, prime):
    """
    like before, but instead has the line intdices as
    they will be if everything is flattened
    """
    indices = lines_for_plane_organization(prime)
    in_place = indices
    for a, _ in enumerate(in_place):
        for b, __ in enumerate(in_place[0]):
            in_place[a][b] = in_place[a][b][0] + in_place[a][b][1] * prime
    return in_place


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
) -> Tuple[List[List[int]], Dict[Tuple[int, ...], int]]:
    final_length: int = prime**4
    place_holder: List[List[int]] = [[] for _ in range(final_length)]
    translator: Dict[Tuple[int, ...], int] = {}
    structured = all_non_flat_lines(prime)
    for x, y, z, w in product(range(prime), repeat=4):
        spot: int = prime**3 * x + prime**2 * y + prime * z + w
        line: List[int] = structured[x][y][z][w]
        place_holder[spot] = structured[x][y][z][w]
        translator[tuple(line)] = spot
    return place_holder, translator


def all_non_flat_plane_groupings_index(non_index_list, translator):
    return [
        [translator[tuple(line)] for line in grouping]
        for grouping in non_index_list
    ]


# Intermediate lines
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


# Final direction
def final_direction(prime: int) -> List[int]:
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
