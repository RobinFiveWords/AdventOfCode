import collections

class IntCode:
  opcodes = {
    1: 'add',
    2: 'mul',
    3: 'inp',
    4: 'out',
    5: 'bne',  # jump-if-true; jump if non-zero
    6: 'beq',  # jump-if-false; jump if zero
    7: 'lt',
    8: 'eq',
    9: 'rel',  # adjust relative base
    99: 'hlt',
  }

  def __init__(self, program):
    self.ram = collections.defaultdict(int)
    for i, n in enumerate(program.strip().split(',')):
      self.ram[i] = int(n)
    self.ip = 0
    self.relative_base = 0
    self.running = False
    self.waiting = False
    self.halted = False
    self.q_in = collections.deque()
    self.q_out = collections.deque()

  def getv(self, position, mode=1):
    value = self.ram[position]
    if mode == 0:  # positional
      return self.ram[value]
    elif mode == 1:  # immediate
      return value
    elif mode == 2:  # relative
      return self.ram[value + self.relative_base]
    else:
      raise ValueError(f'parameter mode {mode} not defined')

  def getd(self, position, mode=0):
    value = self.ram[position]
    if mode == 0:  # positional
      return value
    elif mode == 2:  # relative
      return value + self.relative_base
    else:
      raise ValueError(f'parameter mode {mode} not defined')

  def add(self, modes=''):
    mode1, mode2, mode3 = map(int, (modes + '000')[:3])
    summand1 = self.getv(self.ip + 1, mode1)
    summand2 = self.getv(self.ip + 2, mode2)
    destination = self.getd(self.ip + 3, mode3)
    self.ram[destination] = summand1 + summand2
    self.ip += 4

  def mul(self, modes=''):
    mode1, mode2, mode3 = map(int, (modes + '000')[:3])
    factor1 = self.getv(self.ip + 1, mode1)
    factor2 = self.getv(self.ip + 2, mode2)
    destination = self.getd(self.ip + 3, mode3)
    self.ram[destination] = factor1 * factor2
    self.ip += 4

  def inp(self, modes=''):
    if not self.q_in:
      if self.waiting:
        self.halted = True
      else:
        self.running = False
        self.waiting = True
      return None
    self.waiting = False
    mode = int((modes + '0')[0])
    destination = self.getd(self.ip + 1, mode)
    self.ram[destination] = self.q_in.popleft()
    self.ip += 2

  def out(self, modes=''):
    mode = int((modes + '0')[0])
    value = self.getv(self.ip + 1, mode)
    self.q_out.append(value)
    self.ip += 2

  def bne(self, modes=''):
    mode1, mode2 = map(int, (modes + '00')[:2])
    if self.getv(self.ip + 1, mode1):
      self.ip = self.getv(self.ip + 2, mode2)
    else:
      self.ip += 3

  def beq(self, modes=''):
    mode1, mode2 = map(int, (modes + '00')[:2])
    if not self.getv(self.ip + 1, mode1):
      self.ip = self.getv(self.ip + 2, mode2)
    else:
      self.ip += 3

  def lt(self, modes=''):
    mode1, mode2, mode3 = map(int, (modes + '000')[:3])
    value1 = self.getv(self.ip + 1, mode1)
    value2 = self.getv(self.ip + 2, mode2)
    destination = self.getd(self.ip + 3, mode3)
    self.ram[destination] = 1 if value1 < value2 else 0
    self.ip += 4

  def eq(self, modes=''):
    mode1, mode2, mode3 = map(int, (modes + '000')[:3])
    value1 = self.getv(self.ip + 1, mode1)
    value2 = self.getv(self.ip + 2, mode2)
    destination = self.getd(self.ip + 3, mode3)
    self.ram[destination] = 1 if value1 == value2 else 0
    self.ip += 4

  def rel(self, modes=''):
    mode = int((modes + '0')[0])
    value = self.getv(self.ip + 1, mode)
    self.relative_base += value
    self.ip += 2

  def hlt(self, modes=''):
    self.running = False
    self.halted = True

  def run(self):
    if self.halted:
      return None
    self.running = True
    while not self.halted and self.running:
      op_modes = self.getv(self.ip, 1)  # like immediate mode
      opcode = self.opcodes[op_modes % 100]
      if op_modes < 100:
        getattr(self, opcode)()
      else:
        modes = str(op_modes // 100)[::-1]
        getattr(self, opcode)(modes)

  def __repr__(self):
    return ','.join(str(n) for i, n in sorted(self.ram.items()))
