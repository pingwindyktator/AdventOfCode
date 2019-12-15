from collections import deque
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
            9: self._opcode_update_relative_base,
            99: self._opcode_halt,
        }

    def _opcode_update_relative_base(self, program):
        program.relative_base += program.get_param_value(1)
        program.pc += 2

    def _opcode_add(self, program):
        program.memory[program.get_param_index(3)] = program.get_param_value(1) + program.get_param_value(2)
        program.pc += 4

    def _opcode_mult(self, program):
        program.memory[program.get_param_index(3)] = program.get_param_value(1) * program.get_param_value(2)
        program.pc += 4

    def _opcode_input(self, program):
        program.memory[program.get_param_index(1)] = program.input_func()
        program.pc += 2

    def _opcode_output(self, program):
        try:
            program.output_func(program.get_param_value(1))
        except Exception as e:
            raise e
        finally:
            program.pc += 2

    def _opcode_jump_if_true(self, program):
        if program.get_param_value(1):
            program.pc = program.get_param_value(2)
        else:
            program.pc += 3

    def _opcode_jump_if_false(self, program):
        if not program.get_param_value(1):
            program.pc = program.get_param_value(2)
        else:
            program.pc += 3

    def _opcode_less_than(self, program):
        program.memory[program.get_param_index(3)] = int(program.get_param_value(1) < program.get_param_value(2))
        program.pc += 4

    def _opcode_equals(self, program):
        program.memory[program.get_param_index(3)] = int(program.get_param_value(1) == program.get_param_value(2))
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
        self.memory = self._program_raw + [0] * 5000
        self.pc = 0
        self.result = None
        self.relative_base = 0

    def reset(self):
        self.memory = self._program_raw + [0] * 5000
        self.pc = 0
        self.result = None
        self.relative_base = 0

    def get_opcode(self):
        return int(str(self.memory[self.pc])[-2:])

    def get_param_value(self, index):
        return self.memory[self.get_param_index(index)]

    def get_param_index(self, index):
        param_modes = str(self.memory[self.pc])[:-2][::-1]
        mode = int(param_modes[index - 1] if index <= len(param_modes) else '0')
        if mode == 0:
            return self.memory[self.pc + index]
        elif mode == 1:
            return self.pc + index
        elif mode == 2:
            return self.memory[self.pc + index] + self.relative_base


class repair_droid:
    class _pause_program(Exception):
        pass

    def __init__(self, program_raw):
        self._program_raw = program_raw
        self._current_move = None
        self._position = (0, 0)
        self._neighbours = {}
        self._steps = deque()
        self._oxygen_position = None
        self.program = Intcode_program(self._program_raw, self._get_input, self._set_output)

    def _get_input(self):
        opposite = {1: 2, 2: 1, 3: 4, 4: 3}
        self._neighbours.setdefault(self._position, [None] * 4)

        if None in self._neighbours[self._position]:
            self._current_move = next(i for i, e in enumerate(self._neighbours[self._position]) if e is None) + 1
            self._steps.append(opposite[self._current_move])
            return self._current_move
        else:
            if len(self._steps) == 0: raise self._pause_program
            self._current_move = self._steps.pop()
            return self._current_move

    @staticmethod
    def _get_new_position(position, move):
        delta = {1: (0, 1),
                 2: (0, -1),
                 3: (-1, 0),
                 4: (1, 0)}[move]

        return tuple((position[0] + delta[0], position[1] + delta[1]))

    def _set_output(self, o):
        self._neighbours.setdefault(self._position, [None] * 4)
        self._neighbours[self._position][self._current_move - 1] = o

        if o == 0:
            self._steps.pop()
        elif o == 1:
            self._position = self._get_new_position(self._position, self._current_move)
        elif o == 2:
            self._position = self._get_new_position(self._position, self._current_move)
            self._oxygen_position = self._position

    def run_program(self, computer):
        with suppress(self._pause_program):
            computer.run(self.program)

    def get_longest_path_from_oxygen(self):
        neighbours = {k: [self._get_new_position(k, m + 1) for m in range(4) if v[m] != 0] for k, v in self._neighbours.items()}
        return self._find_longest_path(self._oxygen_position, neighbours)

    @staticmethod
    def _find_longest_path(start, neighbours):
        import sys
        vertices = list(neighbours.keys())
        distances = {v: sys.maxsize for v in vertices}
        distances[start] = 0

        while vertices:
            current = min(vertices, key=lambda v: distances[v])
            if distances[current] == sys.maxsize: break

            for n in neighbours[current]:
                new_route = distances[current] + 1

                if new_route < distances[n]:
                    distances[n] = new_route

            vertices.remove(current)

        return max(distances.values())


if __name__ == '__main__':
    program_raw = list(map(int, open('input').readline().split(',')))
    computer = Intcode_computer()
    droid = repair_droid(program_raw)
    droid.run_program(computer)
    print(droid.get_longest_path_from_oxygen())
