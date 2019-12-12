import math
import re
import itertools
import hashlib
import functools


class moon:
    def __init__(self, position):
        self.position = position
        self.velocity = [0, 0, 0]

    @staticmethod
    def from_str(s):
        return moon(list(int(x) for x in re.findall(r'<x=(-?[0-9]+), y=(-?[0-9]+), z=(-?[0-9]+)>', s)[0]))

    @staticmethod
    def one_step(moons):
        for m, b in itertools.combinations(moons, 2): m.apply_gravity(b)
        for m in moons: m.apply_velocity()

    def apply_gravity(self, other_moon):
        for i in (0, 1, 2):
            if self.position[i] > other_moon.position[i]:
                self.velocity[i] -= 1
                other_moon.velocity[i] += 1
            elif self.position[i] < other_moon.position[i]:
                self.velocity[i] += 1
                other_moon.velocity[i] -= 1

    def apply_velocity(self):
        self.position = [p + v for p, v in zip(self.position, self.velocity)]

    def get_total_energy(self):
        return sum([abs(p) for p in self.position]) * sum([abs(p) for p in self.velocity])


def hash_moons(moons, dim):
    h = hashlib.sha256()
    s = lambda i: str(i).encode()
    for m in moons:
        h.update(s(m.position[dim]))
        h.update(s(m.velocity[dim]))

    return h.digest()


def find_loop(_moons, dim):
    moons = _moons.copy()
    step = 1
    prev_states = {hash_moons(moons, dim)}

    while True:
        moon.one_step(moons)
        hash = hash_moons(moons, dim)
        if hash in prev_states: return step
        prev_states.add(hash)
        step += 1


def ilcm(iterable):
    return functools.reduce(lambda a, b: a * b // math.gcd(a, b), iterable, 1)


if __name__ == '__main__':
    moons = list(map(moon.from_str, open('input').readlines()))
    print(ilcm([find_loop(moons, x) for x in (0, 1, 2)]))
