import re

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

regex_register = re.compile(r'Register ([A-C]): (\d+)')


class Computer:
  opcodes = {
    0: 'adv',
    1: 'bxl',
    2: 'bst',
    3: 'jnz',
    4: 'bxc',
    5: 'out',
    6: 'bdv',
    7: 'cdv',
  }

  def __init__(self, file):
    with open(file) as f:
      sections = f.read().strip().split('\n\n')
    for m in regex_register.finditer(sections[0]):
      label, n = m.groups()
      setattr(self, label.lower(), int(n))  # assigns self.a, self.b, self.c
    self.initial_state = (self.a, self.b, self.c)
    self.program = parse_ints(sections[1])
    self.ip = 0
    self.q_out = []

  def reset(self):
    self.a, self.b, self.c = self.initial_state
    self.ip = 0
    self.q_out = []

  def adv(self, combo_operand):
    """opcode 0"""
    self.a //= 2 ** self.combo(combo_operand)
    self.ip += 2

  def bxl(self, literal_operand):
    """opcode 1"""
    self.b ^= literal_operand
    self.ip += 2

  def bst(self, combo_operand):
    """opcode 2"""
    self.b = self.combo(combo_operand) % 8
    self.ip += 2

  def jnz(self, literal_operand):
    """opcode 3"""
    if self.a != 0:
      self.ip = literal_operand
    else:
      self.ip += 2

  def bxc(self, operand):
    """opcode 4"""
    self.b ^= self.c
    self.ip += 2

  def out(self, combo_operand):
    """opcode 5"""
    self.q_out.append(self.combo(combo_operand) % 8)
    self.ip += 2

  def bdv(self, combo_operand):
    """opcode 6"""
    self.b = self.a // (2 ** self.combo(combo_operand))
    self.ip += 2

  def cdv(self, combo_operand):
    """opcode 7"""
    self.c = self.a // (2 ** self.combo(combo_operand))
    self.ip += 2

  def combo(self, operand):
    if operand <= 3:
      return operand
    if operand == 4:
      return self.a
    if operand == 5:
      return self.b
    if operand == 6:
      return self.c
    raise ValueError

  def run(self, a=None):
    self.reset()
    if a is not None:
      self.a = a
    program_length = len(self.program)
    while 0 <= self.ip < program_length:
      opcode, operand = self.program[self.ip:self.ip+2]
      getattr(self, self.opcodes[opcode])(operand)
    return ','.join(map(str, self.q_out))

  def search(self):
    # in the real input,
    # it seems like whatever value X of A matches the last N digits of the program,
    # the smallest value of A that matches the last N+1 digits of the program
    # is equal to or slightly greater than 8 * X.
    program = ','.join(map(str, self.program))
    a = 0
    while True:
      output = self.run(a)
      if output == program[-len(output):]:
        break
      a += 1
    # found last digit, can now start pattern
    while len(output) < len(program):
      a *= 8
      while True:
        output = self.run(a)
        if output == program[-len(output):]:
          break
        a += 1
    return a


def main():
  print(f'Day {DAY} part 1: {Computer(INPUT_FILE).run()}')
  print(f'Day {DAY} part 2: {Computer(INPUT_FILE).search()}')
  pass

if __name__ == '__main__':
  main()
