import math


def map_to_coords(m):
    result = []
    for y, row in enumerate(m):
        for x, el in enumerate(row.strip()):
            if el != '.': result.append((x, y))

    return result


def degree(a, b):
    x = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) + 90
    return 270 + 90 + x if x < 0 else x


def distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])


def degree_to_coords(coords, start):
    result = {}
    for c, d in {end: degree(start, end) for end in coords}.items():
        result.setdefault(d, list()).append(c)

    return {d: sorted(c, key=lambda coords: distance(start, coords)) for d, c in result.items()}


def vaporize_until(dc, index):
    i = 0
    while i < index:
        for d in [k for k in sorted(dc.keys()) if dc[k]]:
            if i + 1 == index: return dc[d][0]
            dc[d] = dc[d][1:]
            i += 1


def count_visible_asteroids(coords, start):
    return len(set([degree(start, end) for end in coords]))


if __name__ == '__main__':
    coords = map_to_coords(open('input').readlines())
    best_location = max(coords, key=lambda x: count_visible_asteroids(coords, x))
    dc = degree_to_coords(coords, best_location)
    nth_vaporized = vaporize_until(dc, 200)
    print(nth_vaporized[0] * 100 + nth_vaporized[1])
