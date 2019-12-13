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


class arcade_cabinet:
    def __init__(self, program_raw, quarters_inserted):
        self._program_raw = program_raw
        self._program_raw[0] = quarters_inserted
        self._output_type = 0
        self.high_score = None
        self.screen = {}
        self.program = Intcode_program(self._program_raw, self._get_input, self._set_output)

    def _set_output(self, o):
        if self._output_type == 0: self._x = o
        elif self._output_type == 1: self._y = o
        elif self._output_type == 2:
            self._tile_id = o
            if self._x == -1 and self._y == 0: self._set_new_score(self._tile_id)
            else: self._draw_tile((self._x, self._y), self._tile_id)

        self._output_type = (self._output_type + 1) % 3

    def _get_input(self):
        paddle = next((pos for pos, obj in self.screen.items() if obj == 3))
        ball = next((pos for pos, obj in self.screen.items() if obj == 4))
        if paddle[0] == ball[0]: return 0
        if paddle[0] > ball[0]: return -1
        return 1

    def run_program(self, computer):
        computer.run(self.program)

    def _draw_tile(self, position, tile_id):
        self.screen[position] = tile_id

    def _set_new_score(self, score):
        self.high_score = score


if __name__ == '__main__':
    program_raw = list(map(int, open('input').readline().split(',')))
    computer = Intcode_computer()
    arc = arcade_cabinet(program_raw, 2)
    arc.run_program(computer)
    print(arc.high_score)