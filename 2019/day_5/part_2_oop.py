class Intcode_computer:
    class _halt_exception(Exception): pass

    def __init__(self):
        self._memory = None
        self._pc = None
        self._opcodes = {
            1: self._opcode_add,
            2: self._opcode_mult,
            3: self._opcode_input,
            4: self._opcode_output,
            5: self._opcode_jump_if_true,
            6: self._opcode_jump_if_false,
            7: self._opcode_less_than,
            8: self._opcode_equals,
            99: self._opcode_halt,
        }

    def _get_opcode(self):
        return int(str(self._memory[self._pc])[-2:])

    def _get_param(self, index):
        param_modes = str(self._memory[self._pc])[:-2][::-1]
        mode = int(param_modes[index - 1] if index <= len(param_modes) else '0')
        if mode == 0:
            return self._memory[self._memory[self._pc + index]]
        elif mode == 1:
            return self._memory[self._pc + index]

    def _opcode_add(self, _):
        self._memory[self._memory[self._pc + 3]] = self._get_param(1) + self._get_param(2)
        self._pc += 4

    def _opcode_mult(self, _):
        self._memory[self._memory[self._pc + 3]] = self._get_param(1) * self._get_param(2)
        self._pc += 4

    def _opcode_input(self, program):
        self._memory[self._memory[self._pc + 1]] = program.input_func()
        self._pc += 2

    def _opcode_output(self, program):
        program.output_func(self._get_param(1))
        self._pc += 2

    def _opcode_jump_if_true(self, _):
        if self._get_param(1): self._pc = self._get_param(2)
        else: self._pc += 3

    def _opcode_jump_if_false(self, _):
        if not self._get_param(1): self._pc = self._get_param(2)
        else: self._pc += 3

    def _opcode_less_than(self, _):
        self._memory[self._memory[self._pc + 3]] = int(self._get_param(1) < self._get_param(2))
        self._pc += 4

    def _opcode_equals(self, _):
        self._memory[self._memory[self._pc + 3]] = int(self._get_param(1) == self._get_param(2))
        self._pc += 4

    def _opcode_halt(self, _):
        raise self._halt_exception()

    def run(self, program):
        self._memory = program.program.copy()
        self._pc = 0

        while self._pc < len(self._memory):
            opcode = self._get_opcode()
            try:
                self._opcodes[opcode](program)
            except IndexError:
                raise RuntimeError(f'unknown opcode: {opcode}')
            except self._halt_exception:
                return self._memory[0]

    def run_TEST(self, program_raw, unit_under_test_id):
        program = Intcode_program(program_raw, lambda: unit_under_test_id, print)
        return self.run(program)


class Intcode_program:
    def __init__(self, program, input_func, output_func):
        self.program = program
        self.input_func = input_func
        self.output_func = output_func


if __name__ == '__main__':
    program = list(map(int, open('input').readline().split(',')))
    computer = Intcode_computer()
    print(computer.run_TEST(program, 5))
