def find_shortest_path(start, end, neighbours):
    import sys
    vertices = list(neighbours.keys())
    distances = {v: sys.maxsize for v in vertices}
    distances[start] = 0

    while vertices:
        current = min(vertices, key=lambda v: distances[v])
        if distances[current] == sys.maxsize: break

        for n in neighbours[current]:
            new_route = distances[current] + 1

            if new_route < distances[n]:
                distances[n] = new_route

        vertices.remove(current)

    return distances[end]


if __name__ == '__main__':
    neighbours = {}
    for object, orbits_around in list(map(lambda x: [x.strip() for x in x.split(')')], open('input').readlines())):
        if orbits_around not in neighbours: neighbours[orbits_around] = []
        if object not in neighbours: neighbours[object] = []
        neighbours[orbits_around].append(object)
        neighbours[object].append(orbits_around)

    start = neighbours['YOU'][0]
    end = neighbours['SAN'][0]
    print(find_shortest_path(start, end, neighbours))
