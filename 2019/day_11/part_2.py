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


class painting_robot:
    def __init__(self, program_raw, init_pos_color=0):
        self._program_raw = program_raw
        self.current_pos = (0, 0)
        self.current_direction = (0, 1)
        self.panels = {}
        self.panels[self.current_pos] = init_pos_color
        self._output_type = 0
        self.program = Intcode_program(self._program_raw, self._get_current_color, self._set_output)

    def _get_current_color(self):
        return self.panels.setdefault(self.current_pos, 0)

    def _paint_panel(self, color):
        self.panels[self.current_pos] = color

    def _turn(self, direction):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        i = next((i for i in range(len(directions)) if directions[i] == self.current_direction))

        if direction == 0: i -= 1
        elif direction == 1: i = (i + 1) % 4

        self.current_direction = directions[i]
        self.current_pos = (self.current_pos[0] + directions[i][0], self.current_pos[1] + directions[i][1])

    def _set_output(self, o):
        if self._output_type == 0: self._paint_panel(o)
        elif self._output_type == 1: self._turn(o)

        self._output_type = (self._output_type + 1) % 2

    def run_program(self, computer):
        computer.run(self.program)

    def colored_panels(self):
        return len(self.panels)

    def print_panels(self):
        x_offset = min((x for x, _ in self.panels.keys()))
        y_offset = min((y for _, y in self.panels.keys()))
        size = max((max(x, y) for x, y in self.panels.keys()))
        size = max(size + x_offset, size + y_offset) + 1
        result = [[0 for _ in range(size)] for _ in range(size)]

        for x, y in self.panels.keys():
            result[y + y_offset][x + x_offset] = self.panels[(x, y)]

        m = {0: '.', 1: 'o'}
        for r in result[::-1]: print(''.join([m[x] for x in r]))


if __name__ == '__main__':
    program_raw = list(map(int, open('input').readline().split(',')))
    computer = Intcode_computer()
    robot = painting_robot(program_raw, 1)
    robot.run_program(computer)
    robot.print_panels()
