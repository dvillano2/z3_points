from non_flat_lines import (
    non_flat_lines_through_origin,
    non_flat_line_translates,
)
from final_direction import final_line_translates, final_direction


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


def non_vertical_planes(prime, non_flat_direction):
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
        place_holder.extend(non_vertical_planes(prime, direction))
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


def all_plane_groupings(prime):
    non_flat = non_flat_plane_groupings(prime)
    flat = final_line_translates(prime, final_direction(prime))
    non_flat.extend(flat)
    return non_flat


def flattened_non_indexed(non_index_list):
    return [
        [point for line in plane for point in line] for plane in non_index_list
    ]
