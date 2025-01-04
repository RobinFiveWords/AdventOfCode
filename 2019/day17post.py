import re

from IntCode import IntCode
from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'


directions = {
  '^': Up,
  'v': Down,
  '<': Left,
  '>': Right,
}

turns = {
  Up: {Left: 'L', Right: 'R'},
  Right: {Up: 'L', Down: 'R'},
  Down: {Right: 'L', Left: 'R'},
  Left: {Down: 'L', Up: 'R'},
}

# https://www.reddit.com/r/adventofcode/comments/ebr7dg/comment/fb7ymcw/
regex = re.compile(r'^(.{1,21})\1*(.{1,21})(?:\1|\2)*(.{1,21})(?:\1|\2|\3)*$')
# expects extra comma at end
# allows up to 21 because functions are separated by a comma we don't load


class ASCII:
  def __init__(self, file):
    self.points = set()
    self.start = None
    self.facing = None
    self.file = file
    self.A = None
    self.B = None
    self.C = None
    self.Main = None
    self.reset_cpu()

  def reset_cpu(self):
    with open(self.file) as f:
      self.cpu = IntCode(f.read())

  def get_map(self):
    self.cpu.run()
    x = 0
    y = 0
    while self.cpu.q_out:
      c = chr(self.cpu.q_out.popleft())
      if c == '\n':
        y += 1
        x = 0
      elif c == '.':
        x += 1
      elif c == '#':
        self.points.add(Point(x, y))
        x += 1
      elif c in (['^', 'v', '<', '>']):
        point = Point(x, y)
        self.points.add(point)
        self.start = point
        self.facing = directions[c]        
        x += 1
      else:
        raise ValueError(f"{c} observed at ({x}, {y})")

  def sum_alignment_parameters(self):
    result = 0
    for point in self.points:
      if all(point + direction in self.points
             for direction in directions.values()):
        result += point.x * point.y
    return result

  def send(self, s, newline=True):
    for char in s:
      self.cpu.q_in.append(ord(char))
    if newline:
      self.cpu.q_in.append(ord('\n'))

  def compress(self):
    movements = []
    current = self.start
    previous = None
    direction = self.facing
    length = 0
    while True:
      neighbors = {p: d for d in directions.values()
                   if (p := current + d) in self.points
                   and p != previous}
      if not neighbors:
        movements.append(length)
        break
      if current + direction in neighbors:
        length += 1
        previous = current
        current += direction
        continue
      assert len(neighbors) == 1
      if previous:
        movements.append(length)
      neighbor, new_direction = list(neighbors.items())[0]
      turn = turns[direction][new_direction]
      movements.append(turn)
      direction = new_direction
      length = 0
    path = ','.join(map(str, movements))
    m = regex.match(path + ',')
    assert m
    functions = [g[:-1] for g in m.groups()]
    self.A, self.B, self.C = functions
    assert not any([s1.startswith(s2)
                    for s1 in functions
                    for s2 in functions
                    if s1 != s2])
    routine = []
    remaining = path
    while remaining:
      if remaining.startswith(self.A):
        routine.append('A')
        remaining = remaining[len(self.A)+1:]
      elif remaining.startswith(self.B):
        routine.append('B')
        remaining = remaining[len(self.B)+1:]
      elif remaining.startswith(self.C):
        routine.append('C')
        remaining = remaining[len(self.C)+1:]
      else:
        raise ValueError("I thought this path was good?")
    self.Main = ','.join(routine)

  def walk(self, continuous=False):
    self.reset_cpu()
    self.cpu.ip = 0
    self.cpu.ram[0] = 2
    self.cpu.run()
    self.send(self.Main)
    self.send(self.A)
    self.send(self.B)
    self.send(self.C)
    self.send('y' if continuous else 'n')
    self.cpu.run()
    return self.cpu.q_out[-1]


a = ASCII(INPUT_FILE)
a.get_map()

print(f'Day {DAY} part 1: {a.sum_alignment_parameters()}')

a.compress()

print(f'Day {DAY} part 2: {a.walk()}')
