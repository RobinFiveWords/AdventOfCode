import collections

from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')


DIRECTIONS = [Up, Down, Left, Right]


class Farm:
  def __init__(self, file):
    with open(file) as f:
      rows = f.read().strip().split('\n')
    self.min = 0
    self.max = len(rows)
    self.rocks = set()
    self.start = None
    for y, row in enumerate(rows):
      for x, char in enumerate(row):
        if char == 'S':
          self.start = Point(x, y)
        elif char == '#':
          self.rocks.add(Point(x, y))
    self.reset()

  def reset(self):
    self.visited = set()
    self.visited.add(self.start)
    self.even = set()
    self.even.add(self.start)
    self.even_counts = {0: len(self.even)}
    self.odd = set()
    self.odd_counts = {}

  def steps(self, N):
    self.reset()
    last = [self.start]
    pending = set()
    for step in range(1, N + 1):
      for last_point in last:
        for direction in DIRECTIONS:
          new_point = last_point + direction
          if new_point.x < self.min or new_point.x >= self.max:
            continue
          if new_point.y < self.min or new_point.y >= self.max:
            continue
          if new_point in self.visited or new_point in self.rocks:
            continue
          self.visited.add(new_point)
          pending.add(new_point)
      if step % 2 == 0:
        self.even.update(pending)
        self.even_counts[step] = len(self.even)
      else:
        self.odd.update(pending)
        self.odd_counts[step] = len(self.odd)
      last = list(pending)
      pending = set()
    return len(self.even)


test_farm = Farm(TEST_INPUT_FILE)
assert test_farm.steps(6) == 16

real_farm = Farm(INPUT_FILE)
print(f'Day {DAY} part 1: {real_farm.steps(64)}')


class ExpandedFarm(Farm):
  def expand(self):
    starting_rocks = set(self.rocks)
    offsets = [
      (Up * 2 + Left * 1) * 131,
      (Up * 2) * 131,
      (Up * 2 + Right * 1) * 131,
      (Up * 1 + Left * 2) * 131,
      (Up * 1 + Left * 1) * 131,
      (Up * 1) * 131,
      (Up * 1 + Right * 1) * 131,
      (Up * 1 + Right * 2) * 131,
      (Left * 2) * 131,
      (Left * 1) * 131,
      (Right * 1) * 131,
      (Right * 2) * 131,
      (Down * 1 + Left * 2) * 131,
      (Down * 1 + Left * 1) * 131,
      (Down * 1) * 131,
      (Down * 1 + Right * 1) * 131,
      (Down * 1 + Right * 2) * 131,
      (Down * 2 + Left * 1) * 131,
      (Down * 2) * 131,
      (Down * 2 + Right * 1) * 131,
    ]
    for offset in offsets:
      for rock in starting_rocks:
        self.rocks.add(rock + offset)
    self.min = -999
    self.max = 999

  def run(self):
    self.steps(131 * 2 + 65)
    squares = collections.Counter()
    for endpoint in self.odd:
      squares[(endpoint.x // 131, endpoint.y // 131)] += 1

    center_even = 1
    center_odd = 0
    for i in range(1, 202300):
      if i % 2 == 1:
        center_odd += 4 * i
      else:
        center_even += 4 * i

    frequencies = {
      (0, 0): center_even,
      (1, 0): center_odd,
      (0, 2): 1,
      (2, 0): 1,
      (0, -2): 1,
      (-2, 0): 1,
      (2, 1): 202300,
      (1, 1): 202299,
      (2, -1): 202300,
      (1, -1): 202299,
      (-2, 1): 202300,
      (-1, 1): 202299,
      (-2, -1): 202300,
      (-1, -1): 202299,
    }

    return sum(squares[square] * frequency
               for square, frequency in frequencies.items())


ef = ExpandedFarm(INPUT_FILE)
ef.expand()
print(f'Day {DAY} part 2: {ef.run()}')


# in 130 moves from S we can reach any garden plot on main map
# we always have a clear path to reach S, so we can move to any S directly
# divmod(26501365, 131) = (202300, 65)
# so we can move any combination of U, D, L, R 202300-ish times
# note that the parity flips each time
# and that we want the odd counts for part 2, NOT THAT I MADE THIS MISTAKE, OF COURSE
# what can we reach along the fringe?
# try a 1-2-3-4-3-2-1 and 131 * 2 + 65 steps

# how many of each kind of square?
# this is where my display_points function comes in handy, particularly as
# display_points(ef.odd | ef.rocks)
# to view in context of the repeated map

# CENTER EVEN                                     Base
# 8 * triangle(101149) + 1

# CENTER ODD                                      Right * 1
# 4 * triangle(202299) - 8 * triangle(101149)

# 1      POINT DOWN                               Down * 2
# 1      POINT UP                                 Up * 2
# 1      POINT LEFT                               Left * 2
# 1      POINT RIGHT                              Right * 2
# 202300 bottom-right side, UPPER LEFT ONLY       Down * 1 + Right * 2
# 202299 bottom-right side, ALL BUT BOTTOM RIGHT  Down * 1 + Right * 1
# 202300 top-right side, BOTTOM LEFT ONLY         Up * 1 + Right * 2
# 202299 top-right side, ALL BUT TOP RIGHT        Up * 1 + Right * 1
# 202300 bottom-left side, UPPER RIGHT ONLY       Down * 1 + Left * 2
# 202299 bottom-left side, ALL BUT BOTTOM LEFT    Down * 1 + Left * 1
# 202300 top-left side, BOTTOM RIGHT ONLY         Up * 1 + Left * 2
# 202299 top-left side, ALL BUT TOP LEFT          Up * 1 + Left * 2
