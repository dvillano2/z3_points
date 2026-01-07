from itertools import product
from final_direction import final_line_translates, final_direction
from non_flat_lines import single_list_non_flat_lines
from intermediate_lines import all_intermediate_lines
from planes import all_plane_groupings, flattened_non_indexed


def full_line_list(prime: int):
    line_list = single_list_non_flat_lines(prime)
    intermediate = all_intermediate_lines(prime)
    for x, y, z in product(range(prime), repeat=3):
        spot = prime**4 + prime**2 * x + prime * y + z
        line = intermediate[x][y][z]
        assert len(line_list) == spot
        line_list.append(line)
    final = final_line_translates(prime, final_direction(prime))
    for x, y in product(range(prime), repeat=2):
        spot = prime**4 + prime**3 + prime * x + y
        line = final[x][y]
        assert len(line_list) == spot
        line_list.append(line)
    return line_list


def build_geometry(prime):
    line_list = full_line_list(prime)
    non_indexed = all_plane_groupings(prime)
    flattened = flattened_non_indexed(non_indexed)
    return line_list, flattened
