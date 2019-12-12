import re
import itertools


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


if __name__ == '__main__':
    moons = list(map(moon.from_str, open('input').readlines()))
    for _ in range(1000): moon.one_step(moons)
    print(sum([a.get_total_energy() for a in moons]))
