import numpy as np

from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

EMPTY = 0
WALL = 1
BOX = 2
ROBOT = 3
BOXL = 4
BOXR = 5

DISPLAY = {
  EMPTY: '.',
  WALL: '#',
  BOX: 'O',
  ROBOT: '@',
  BOXL: '[',
  BOXR: ']',
}

MOVEMENTS = {
  '^': Up,
  '>': Right,
  'v': Down,
  '<': Left,
}


class Warehouse:
  def __init__(self, file):
    with open(file) as f:
      _map, movements = f.read().strip().split('\n\n')

    self.r = None
    self.walls = set()
    self.starting_boxes = set()
    for y, line in enumerate(_map.split('\n')):
      for x, char in enumerate(line):
        point = Point(x, y)
        if char == '#':
          self.walls.add(point)
        elif char == 'O':
          self.starting_boxes.add(point)
        elif char == '@':
          self.r = point
    self.a = np.zeros((y + 1, x + 1), dtype=np.int8)
    for point in self.walls:
      self.a[point.y, point.x] = WALL
    for point in self.starting_boxes:
      self.a[point.y, point.x] = BOX

    self.movements = [MOVEMENTS[char] for char in movements.replace('\n', '')]

  def display(self):
    for y, line in enumerate(self.a):
      for x, value in enumerate(line):
        if self.r == Point(x, y):
          assert value == 0
          value = ROBOT
        print(DISPLAY[value], end='')
      print()

  def move(self, direction):
    R = self.r + direction
    if self.a[R.y, R.x] == EMPTY:
      self.r = R
      return
    if self.a[R.y, R.x] == WALL:
      return
    if direction == Up:
      a = self.a[:self.r.y, self.r.x][::-1]
    elif direction == Right:
      a = self.a[self.r.y, self.r.x + 1:]
    elif direction == Down:
      a = self.a[self.r.y + 1:, self.r.x]
    elif direction == Left:
      a = self.a[self.r.y, :self.r.x][::-1]
    else:
      raise ValueError(f'unexpected direction {direction}')
    moved = push(a)
    if moved:
      self.r = R

  def execute(self):
    for direction in self.movements:
      self.move(direction)
    return self.gps()

  def gps(self):
    result = 0
    for y, line in enumerate(self.a):
      for x, value in enumerate(line):
        if value == BOX:
          result += 100 * y + x
    return result


def push(a):
  # find first wall or empty; if wall, do nothing; if empty, push boxes
  index = np.nonzero(a != BOX)[0][0]  # wall border guarantees non-empty
  val = a[index]
  if val == EMPTY:
    a[:index + 1] = np.roll(a[:index + 1], 1)
    return True
  return False


class Warehouse2:
  def __init__(self, file):
    with open(file) as f:
      _map, movements = f.read().strip().split('\n\n')

    self.r = None
    self.walls = set()
    self.starting_boxesL = set()
    self.starting_boxesR = set()
    for y, line in enumerate(_map.split('\n')):
      for x1, char in enumerate(line):
        x = x1 * 2
        pointL = Point(x, y)
        x += 1
        pointR = Point(x, y)
        if char == '#':
          self.walls.add(pointL)
          self.walls.add(pointR)
        elif char == 'O':
          self.starting_boxesL.add(pointL)
          self.starting_boxesR.add(pointR)
        elif char == '@':
          self.r = pointL
    self.a = np.zeros((y + 1, x + 1), dtype=np.int8)
    for point in self.walls:
      self.a[point.y, point.x] = WALL
    for point in self.starting_boxesL:
      self.a[point.y, point.x] = BOXL
    for point in self.starting_boxesR:
      self.a[point.y, point.x] = BOXR

    self.movements = [MOVEMENTS[char] for char in movements.replace('\n', '')]

  def display(self):
    for y, line in enumerate(self.a):
      for x, value in enumerate(line):
        if self.r == Point(x, y):
          assert value == 0
          value = ROBOT
        print(DISPLAY[value], end='')
      print()

  def move(self, direction):
    R = self.r + direction
    destination = self.a[R.y, R.x]
    if destination == EMPTY:
      self.r = R
      return
    if destination == WALL:
      return
    if direction == Right:
      a = self.a[self.r.y, self.r.x + 1:]
      moved = push2horizontal(a)
      if moved:
        self.r = R
      return
    elif direction == Left:
      a = self.a[self.r.y, :self.r.x][::-1]
      moved = push2horizontal(a)
      if moved:
        self.r = R
      return
    # for push vertical, track all potentially pushed boxes
    # until frontier of x coords hits **any** wall or **all** empty
    elif direction == Up:
      if destination == BOXL:
        point2 = R + Right
      elif destination == BOXR:
        point2 = R + Left
      else:
        raise ValueError(f"unexpected contents {destination} in {n}")
      pushing = [R, point2]
      frontier = pushing[:]
      pending = set()
      while frontier:
        for box in frontier:
          n = box + Up
          contents = self.a[n.y, n.x]
          if contents == WALL:
            return
          if contents == EMPTY:
            continue
          if contents == BOXL:
            point2 = n + Right
          elif contents == BOXR:
            point2 = n + Left
          else:
            raise ValueError(f"unexpected contents {destination} in {n}")
          pushing.extend([n, point2])
          pending.update([n, point2])
        frontier = list(pending)
        pending = set()
      to_move = sorted((point.y, point.x, self.a[point.y, point.x])
                       for point in pushing)
      for y, x, value in to_move:
        self.a[y - 1, x] = value
        self.a[y, x] = EMPTY
      self.r = R
    elif direction == Down:
      if destination == BOXL:
        point2 = R + Right
      elif destination == BOXR:
        point2 = R + Left
      else:
        raise ValueError(f"unexpected contents {destination} in {n}")
      pushing = [R, point2]
      frontier = pushing[:]
      pending = set()
      while frontier:
        for box in frontier:
          n = box + Down
          contents = self.a[n.y, n.x]
          if contents == WALL:
            return
          if contents == EMPTY:
            continue
          if contents == BOXL:
            point2 = n + Right
          elif contents == BOXR:
            point2 = n + Left
          else:
            raise ValueError(f"unexpected contents {destination} in {n}")
          pushing.extend([n, point2])
          pending.update([n, point2])
        frontier = list(pending)
        pending = set()
      to_move = sorted(((point.y, point.x, self.a[point.y, point.x])
                        for point in pushing),
                       reverse=True)
      for y, x, value in to_move:
        self.a[y + 1, x] = value
        self.a[y, x] = EMPTY
      self.r = R
    else:
      raise ValueError(f'unexpected direction {direction}')

  def execute(self):
    for direction in self.movements:
      self.move(direction)
    return self.gps()

  def gps(self):
    result = 0
    for y, line in enumerate(self.a):
      for x, value in enumerate(line):
        if value == BOXL:
          result += 100 * y + x
    return result


def push2horizontal(a):
  # find first wall or empty; if wall, do nothing; if empty, push boxes
  index = np.nonzero(~np.isin(a, [BOXL, BOXR]))[0][0]  # wall border guarantees non-empty
  val = a[index]
  if val == EMPTY:
    a[:index + 1] = np.roll(a[:index + 1], 1)
    return True
  return False


def main():
  print(f'Day {DAY} part 1: {Warehouse(INPUT_FILE).execute()}')
  print(f'Day {DAY} part 2: {Warehouse2(INPUT_FILE).execute()}')
  pass

if __name__ == '__main__':
  main()
