def get_param(program, pc, index):
    param_modes = str(program[pc])[:-2][::-1]
    mode = int(param_modes[index - 1] if index <= len(param_modes) else '0')
    if mode == 0:
        return program[program[pc + index]]
    elif mode == 1:
        return program[pc + index]


def process_program(program, input_func, output_func):
    pc = 0
    while pc < len(program):
        opcode = int(str(program[pc])[-2:])
        param = lambda i: get_param(program, pc, i)
        if opcode == 1:
            program[program[pc + 3]] = param(1) + param(2)
            pc += 4
        elif opcode == 2:
            program[program[pc + 3]] = param(1) * param(2)
            pc += 4
        elif opcode == 3:
            program[program[pc + 1]] = input_func()
            pc += 2
        elif opcode == 4:
            output_func(param(1))
            pc += 2
        elif opcode == 5:
            if param(1): pc = param(2)
            else: pc += 3
        elif opcode == 6:
            if not param(1): pc = param(2)
            else: pc += 3
        elif opcode == 7:
            program[program[pc + 3]] = int(param(1) < param(2))
            pc += 4
        elif opcode == 8:
            program[program[pc + 3]] = int(param(1) == param(2))
            pc += 4
        elif opcode == 99:
            return program[0]
        else:
            raise RuntimeError('something went wrong')


def run_TEST(program, unit_under_test_id):
    return process_program(program, lambda: unit_under_test_id, print)


if __name__ == '__main__':
    program = list(map(int, open('input').readline().split(',')))
    print(run_TEST(program, 5))
