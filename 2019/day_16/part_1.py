def get_pattern(index):
    base_pattern = [0, 1, 0, -1]
    index += 1
    result = []
    for p in base_pattern: result.extend([p] * index)
    return result


def get_pattern_index(pattern, index):
    if index < len(pattern) - 1: return index + 1
    return (index + 1) % len(pattern)


def get_next_el(input_signal, pattern):
    result = sum([e * pattern[get_pattern_index(pattern, i)] for i, e in enumerate(input_signal)])
    return abs(result) % 10


def one_phase(input_signal):
    result = []

    for i in range(len(input_signal)):
        pattern = get_pattern(i)
        result.append(get_next_el(input_signal, pattern))

    return result


def n_phases(input_signal, n):
    for _ in range(n): input_signal = one_phase(input_signal)

    return ''.join(map(str, input_signal))


if __name__ == '__main__':
    input_signal = list(map(int, open('input').readline()))
    print(n_phases(input_signal, 100)[:8])

