from shapely.geometry import LineString


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


if __name__ == '__main__':
    wires = list(map(lambda wire: wire_to_LineString(wire.split(',')), open('input').readlines()))
    intersections = wires[0].intersection(wires[1])[1:]
    print(min(map(lambda ip: int(abs(ip.x) + abs(ip.y)), intersections)))
