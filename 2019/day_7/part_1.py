import itertools
from contextlib import suppress


class Intcode_computer:
    class _halt_exception(Exception):
        pass

    def __init__(self):
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

    def _opcode_add(self, program):
        program.memory[program.memory[program.pc + 3]] = program.get_param(1) + program.get_param(2)
        program.pc += 4

    def _opcode_mult(self, program):
        program.memory[program.memory[program.pc + 3]] = program.get_param(1) * program.get_param(2)
        program.pc += 4

    def _opcode_input(self, program):
        program.memory[program.memory[program.pc + 1]] = program.input_func()
        program.pc += 2

    def _opcode_output(self, program):
        try:
            program.output_func(program.get_param(1))
        except Exception as e:
            raise e
        finally:
            program.pc += 2

    def _opcode_jump_if_true(self, program):
        if program.get_param(1):
            program.pc = program.get_param(2)
        else:
            program.pc += 3

    def _opcode_jump_if_false(self, program):
        if not program.get_param(1):
            program.pc = program.get_param(2)
        else:
            program.pc += 3

    def _opcode_less_than(self, program):
        program.memory[program.memory[program.pc + 3]] = int(program.get_param(1) < program.get_param(2))
        program.pc += 4

    def _opcode_equals(self, program):
        program.memory[program.memory[program.pc + 3]] = int(program.get_param(1) == program.get_param(2))
        program.pc += 4

    def _opcode_halt(self, _):
        raise self._halt_exception()

    def run(self, program, restart=False):
        if restart: program.reset()

        while program.pc < len(program.memory):
            opcode = program.get_opcode()
            try:
                self._opcodes[opcode](program)
            except IndexError:
                raise RuntimeError(f'unknown opcode: {opcode}')
            except self._halt_exception:
                program.result = program.memory[0]
                return program.result
            except Exception as e:
                raise e


class Intcode_program:
    def __init__(self, program_raw, input_func, output_func):
        self._program_raw = program_raw
        self.input_func = input_func
        self.output_func = output_func
        self.reset()
        self.memory = self._program_raw
        self.pc = 0
        self.result = None

    def reset(self):
        self.memory = self._program_raw
        self.pc = 0
        self.result = None

    def get_opcode(self):
        return int(str(self.memory[self.pc])[-2:])

    def get_param(self, index):
        param_modes = str(self.memory[self.pc])[:-2][::-1]
        mode = int(param_modes[index - 1] if index <= len(param_modes) else '0')
        if mode == 0:
            return self.memory[self.memory[self.pc + index]]
        elif mode == 1:
            return self.memory[self.pc + index]


class Amplifier:
    class _pause_program(Exception):
        pass

    def __init__(self, phase, program_raw, connected_input_amp=None, init_input=None):
        self.init_input = init_input
        self.connected_input_amp = connected_input_amp
        self._phase = phase
        self._program_raw = program_raw
        self._output = None
        self._input_gen = self._input_generator()
        self.last_output = None
        self.program = Intcode_program(self._program_raw, self._get_input, self._set_output)

    def get_result(self):
        return self.program.result

    def get_output(self):
        o = self._output
        self._output = None
        return o

    def _input_generator(self):
        yield self._phase
        if self.init_input is not None: yield self.init_input
        while True:
            yield self.connected_input_amp.get_output()

    def _get_input(self):
        result = next(self._input_gen)
        if result is not None: return result
        else: raise self._pause_program()

    def _set_output(self, o):
        self._output = o
        self.last_output = o
        raise self._pause_program()

    def run_program(self, computer):
        if self.get_result(): return

        with suppress(self._pause_program):
            computer.run(self.program)


def get_thruster_signal(phases, program_raw, computer):
    A = Amplifier(phases[0], program_raw, init_input=0)
    B = Amplifier(phases[1], program_raw, A)
    C = Amplifier(phases[2], program_raw, B)
    D = Amplifier(phases[3], program_raw, C)
    E = Amplifier(phases[4], program_raw, D)
    for amp in [A, B, C, D, E]:
        amp.run_program(computer)

    return E.last_output


if __name__ == '__main__':
    program_raw = list(map(int, open('input').readline().split(',')))
    computer = Intcode_computer()

    print(max([get_thruster_signal(phases, program_raw, computer) for phases in itertools.permutations([0, 1, 2, 3, 4])]))
