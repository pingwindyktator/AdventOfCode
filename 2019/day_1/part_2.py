def calc_fuel(mass):
    f = int(mass) // 3 - 2
    return f + calc_fuel(f) if f > 0 else 0


if __name__ == '__main__':
    print(sum(list(map(calc_fuel, open('input').readlines()))))
