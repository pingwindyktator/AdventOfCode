from itertools import groupby


def may_be_password(number):
    number = str(number)

    return len(str(number)) == 6 and \
           any((len(list(a)) == 2 for _, a in groupby(number))) and \
           all((a <= b for a, b in zip(number, number[1:])))


if __name__ == '__main__':
    input_range = (138241, 674034)
    print(sum((may_be_password(number) for number in range(input_range[0], input_range[1] + 1))))
