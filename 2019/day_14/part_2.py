import math


class solver:
    def __init__(self, reactions):
        self.reactions = reactions
        self._ingredients = {}
        self._wasted = {}

    @staticmethod
    def from_str(s):
        def to_pair(x):
            x = x.strip().split()
            return tuple((int(x[0]), x[1]))

        result = {}
        for r in s:
            r = r.strip().split('=>')
            result[to_pair(r[1])] = [to_pair(x) for x in r[0].split(',')]

        return solver(result)

    def solve(self, max_ore):
        a = 1
        b = max_ore

        while abs(a - b) > 1:
            pivot = int((a + b) / 2)
            r = self._solve_one(pivot)
            if r > max_ore:
                b = pivot
            else:
                a = pivot

        return a if r > max_ore else b

    def _solve_one(self, _amount):
        self._wasted = {}
        self._ingredients = self._get_ingredients_for(_amount, 'FUEL')

        while not self._solved():
            new_ingredients = {}
            for chem, amount in self._ingredients.items():
                new_ingredients = self._join_ingredients(new_ingredients, self._get_ingredients_for(amount, chem))

            self._ingredients = new_ingredients

        return list(self._ingredients.values())[0]

    def _get_ingredients_for(self, amount_needed, chem):
        if chem == 'ORE': return {'ORE': amount_needed}
        if self._wasted.setdefault(chem, 0) > 0:
            amount_restored = min(amount_needed, self._wasted[chem])
            self._wasted[chem] -= amount_restored
            amount_needed -= amount_restored

        if amount_needed == 0: return {}
        key = next((k for k, v in self.reactions.items() if k[1] == chem))
        amount = key[0]
        ingredients = self.reactions[key]
        multiplier = math.ceil(amount_needed / amount)
        produced_amount = amount * multiplier

        if produced_amount > amount_needed: self._wasted[chem] = self._wasted.setdefault(chem, 0) + (produced_amount - amount_needed)
        return {ing[1]: ing[0] * multiplier for ing in ingredients}

    def _join_ingredients(self, a, b):
        result = a.copy()
        for k, v in b.items(): result[k] = v + result.setdefault(k, 0)
        return result

    def _solved(self):
        return len(self._ingredients) == 1 and list(self._ingredients.keys())[0] == 'ORE'


if __name__ == '__main__':
    s = solver.from_str(open('input').readlines())
    print(s.solve(1000000000000))
