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


def restore_1202_program_alert(_program):
    program = _program.copy()
    program[1] = 76
    program[2] = 3
    return program


if __name__ == '__main__':
    program = list(map(int, open('input').readline().split(',')))
    program = restore_1202_program_alert(program)
    print(process_program(program))
