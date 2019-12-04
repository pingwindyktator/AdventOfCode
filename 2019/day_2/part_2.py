def process_program(program):
    pc = 0
    while pc < len(program):
        if program[pc] == 1:
            program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
            pc += 4
        elif program[pc] == 2:
            program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
            pc += 4
        elif program[pc] == 99:
            return program[0]
        else:
            raise RuntimeError('something went wrong')


def set_program_state(_program, noun, verb):
    program = _program.copy()
    program[1] = noun
    program[2] = verb
    return program


def brute_force_it(program, result_to_find):
    for noun in range(0, 100):
        for verb in range(0, 100):
            if process_program(set_program_state(program, noun, verb)) == result_to_find:
                return noun, verb

    raise RuntimeError('something else went wrong')


if __name__ == '__main__':
    program = list(map(int, open('input').readline().split(',')))
    noun, verb = brute_force_it(program, 19690720)
    print(100 * noun + verb)
