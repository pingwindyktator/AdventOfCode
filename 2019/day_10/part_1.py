import math


def map_to_coords(m):
    result = []
    for y, row in enumerate(m):
        for x, el in enumerate(row.strip()):
            if el != '.': result.append((x, y))

    return result


def degree(a, b):
    return math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])) + 90


def count_visible_asteroids(coords, start):
    return len(set([degree(start, end) for end in coords]))


if __name__ == '__main__':
    coords = map_to_coords(open('input').readlines())
    print(max([count_visible_asteroids(coords, x) for x in coords]))
