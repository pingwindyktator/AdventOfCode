def get_orbits(object, orbits):
    result = []
    while object in orbits:
        result.append(orbits[object])
        object = orbits[object]

    return result


if __name__ == '__main__':
    orbits = {b.strip(): a for a, b in map(lambda x: x.split(')'), open('input').readlines())}
    result = {x: get_orbits(x, orbits) for x in orbits.keys()}

    start = result['YOU'][::-1]
    end = result['SAN'][::-1]
    print(len(start) + len(end) - (2 * len([1 for x, y in zip(start, end) if x == y])))
