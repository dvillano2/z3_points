"""
SOMETHING WRONG... get plane count correct
OVERCOUNTING ON PLANES... each plane is counted 5 times


usage at non flat stage:
line_list, translator = single_list_non_flat_lines(prime)
non_indexed = all_plane_groupings(5)
indexed = indexed_from_non_indexed(non_indexed, translator)
n_indexed = all_plane_groupings(prime)

line_list will be a list of all lines (list of lists)
indexed will be a list of lists where each element represents a
line via its spot in line_list

so for the program, you can sum over everything in the line list
(zeros, ones) demand that they're below the bound, then sum each
of those via the plane groupings and demand they're under p + 1
and the score bumps up if you get the same answer fo
every chunk of the form [kp:(k+1)p]

new usage, for everything:


line_list, translator = full_line_list(prime)
non_indexed = all_plane_groupings(prime)
planes_with_line_indices = indexed_from_non_indexed(non_indexed, translator)
"""

from typing import List
from typing import Dict
from typing import Tuple
from itertools import product


def build_geometry(prime):
    line_list, translator = full_line_list(prime)
    non_indexed = all_plane_groupings(prime)
    planes_with_line_indices = indexed_from_non_indexed(
        non_indexed, translator
    )
    return line_list, planes_with_line_indices


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


def x_lines(prime):
    x_function_lines = [
        [
            [[x, ((m * x) + b) % prime] for x in range(prime)]
            for b in range(prime)
        ]
        for m in range(prime)
    ]
    final_list = [[] for _ in range(prime**2)]
    for a in range(prime):
        for b in range(prime):
            final_list[a + prime * b] = x_function_lines[b][a]
    return final_list


def vertical_lines(prime):
    return [[[y, b] for y in range(prime)] for b in range(prime)]


def reused_directions(prime):
    through_origin = non_flat_lines_through_origin(prime)
    return [planes[0] for planes in through_origin]


def special_directions(prime):
    return non_flat_lines_through_origin(prime)[0]


def non_vertial_planes(prime, non_flat_direction):
    translates = non_flat_line_translates(non_flat_direction, prime)
    in_place = x_lines(prime)
    for a in range(prime**2):
        for b in range(prime):
            in_place[a][b] = translates[in_place[a][b][1]][in_place[a][b][0]]
    return in_place


def reused_plane_groupings(prime):
    through_origin = reused_directions(prime)
    place_holder = []
    for direction in through_origin:
        place_holder.extend(non_vertial_planes(prime, direction))
    return place_holder


def non_flat_plane_groupings(prime):
    reused = reused_plane_groupings(prime)

    through_origin = special_directions(prime)
    for direction in through_origin:
        translates = non_flat_line_translates(direction, prime)
        in_place = vertical_lines(prime)
        for a in range(prime):
            for b in range(prime):
                in_place[a][b] = translates[in_place[a][b][0]][
                    in_place[a][b][1]
                ]
        reused.extend(in_place)
    return reused


def normal_directions(prime):
    """
    gives the normal diretions for the above p^2 + p planes
    every p in the above list is a translation of someting
    normal to the corresponding directions here
    (work in chunks [kp:(k+1)p])
    """
    final_list = []
    for z, x in product(range(prime), repeat=2):
        final_list.append((x, -1, z))
    for z in range(prime):
        final_list.append((1, 0, -z))
    return final_list


def double_check(paired):
    """
    paired should be an expanded version of the
    non_flat_plane_groupings function (apply expand index)
    then repeat all the normal directions above p times
    5 is hardcoded here, change if necessary
    5 becomes prime, 125 becomes prime**2
    """
    count = 0
    tracker = 0
    for plane, normal in paired:
        flattened_plane = [point for line in plane for point in line]
        dot_product = [
            (
                normal[0] * point[0]
                + normal[1] * point[1]
                + normal[2] * point[2]
            )
            % 5
            for point in flattened_plane
        ]
        print(dot_product)
        assert len(set(dot_product)) == 1
        assert len(dot_product) == 25
        print("count:", count)
        assert dot_product[0] == count
        if tracker < 125:
            count = (count - 1) % 5
        else:
            count = (count + 1) % 5
        print(tracker)
        tracker += 1


def all_plane_groupings(prime):
    non_flat = non_flat_plane_groupings(prime)
    flat = final_line_translates(prime, final_direction(prime))
    non_flat.extend(flat)
    return non_flat


def planes_from_line(non_flat_direction, prime):
    """
    THIS OVERCOUNTS
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


def indexed_from_non_indexed(non_index_list, translator):
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


# All together
def full_non_indexed_planes(prime: int):
    non_index = all_non_flat_plane_groupings(prime)
    non_index.extend(final_line_translates(prime, final_direction(prime)))
    return non_index


def full_line_list(prime: int):
    line_list, translator = single_list_non_flat_lines(prime)
    intermediate = all_intermediate_lines(prime)
    for x, y, z in product(range(prime), repeat=3):
        spot = prime**4 + prime**2 * x + prime * y + z
        line = intermediate[x][y][z]
        assert len(line_list) == spot
        line_list.append(line)
        translator[tuple(line)] = spot
    final = final_line_translates(prime, final_direction(prime))
    for x, y in product(range(prime), repeat=2):
        spot = prime**4 + prime**3 + prime * x + y
        line = final[x][y]
        assert len(line_list) == spot
        line_list.append(line)
        translator[tuple(line)] = spot
    return line_list, translator
