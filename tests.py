from utils import expand_index

def test_lines(line_list, prime):
    total_lines = (prime**2 + prime + 1) * prime**2
    line_set = {tuple(line) for line in line_list}
    assert len(line_set) == total_lines

    for line in line_list:
        expanded = [expand_index(point, prime) for point in line]
        assert len({tuple(expand) for expand in expanded}) == prime
        diff = [(c0 - c1) % prime for c0, c1 in zip(expanded[0], expanded[1])]
        assert any(d != 0 for d in diff)
        scales = {
            tuple((s * d) % prime for d in diff) for s in range(1, prime)
        }
        for point in expanded[2:]:
            diff_vec = tuple(
                (c0 - c1) % prime for c0, c1 in zip(expanded[0], point)
            )
            assert diff_vec in scales


def test_planes(plane_list, normal_list, prime):
    total_normals = prime**2 + prime + 1
    total_planes = total_normals * prime
    assert len(set(normal_list)) == total_normals
    assert all(any(c % prime != 0 for c in normal) for normal in normal_list)
    for i, normal_0 in enumerate(normal_list):
        for normal_1 in normal_list[i + 1 :]:
            for scale in range(1, prime):
                assert any(
                    (n0 - scale * n1) % prime != 0
                    for n0, n1 in zip(normal_0, normal_1)
                )

    plane_set = {tuple(plane) for plane in plane_list}
    assert len(plane_set) == total_planes

    expanded_normals = [normal for normal in normal_list for _ in range(prime)]

    intercepts = [0 for _ in range(prime)]
    for plane, normal in zip(plane_list, expanded_normals):
        expanded_plane = [expand_index(point, prime) for point in plane]
        assert len({tuple(expand) for expand in expanded_plane}) == prime**2
        dots = []
        for point in expanded_plane:
            dot = sum(cp * cn for cp, cn in zip(point, normal)) % prime
            dots.append(dot)
        assert len(set(dots)) == 1
        intercepts[dot] += 1
        assert max(intercepts) - min(intercepts) < 2


def test_special_points(prime):
    assert expand_index(0, prime) == (0, 0, 0)
    assert expand_index(1, prime) == (1, 0, 0)
    assert expand_index(prime, prime) == (0, 1, 0)
    assert expand_index(prime**2, prime) == (0, 0, 1)
