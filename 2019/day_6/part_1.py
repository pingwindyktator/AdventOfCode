def get_orbits_count(object, orbits):
    return len(orbits[object]) + sum([get_orbits_count(x, orbits) for x in orbits[object]]) if object in orbits else 0


if __name__ == '__main__':
    orbits = {b.strip(): [a] for a, b in map(lambda x: x.split(')'), open('input').readlines())}
    result = {x: get_orbits_count(x, orbits) for x in orbits.keys()}

    print(sum(result.values()))
