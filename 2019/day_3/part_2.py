from shapely.geometry import LineString, Point


def wire_to_LineString(wire):
    result = [(0, 0)]
    for w in wire:
        direction = w[0]
        length = int(w[1:])
        new = {'U': (0, length),
               'D': (0, -length),
               'R': (length, 0),
               'L': (-length, 0)}[direction]

        result.append((result[-1][0] + new[0], result[-1][1] + new[1]))

    return LineString(result)


def LineString_to_segments(ls):
    result = list(zip(*ls.xy))
    return [(Point(a), Point(b)) for a, b in zip(result, result[1:])]


def count_steps(segments, ip):
    result = 0
    for a, b in segments:
        if LineString([a, b]).distance(ip) == 0:
            result += a.distance(ip)
            return int(result)
        else:
            result += a.distance(b)


if __name__ == '__main__':
    wires = list(map(lambda wire: wire_to_LineString(wire.split(',')), open('input').readlines()))
    segments = [LineString_to_segments(w) for w in wires]
    intersections = wires[0].intersection(wires[1])[1:]
    print(min(map(lambda ip: count_steps(segments[0], ip) + count_steps(segments[1], ip), intersections)))
