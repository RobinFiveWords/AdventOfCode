import collections
import heapq
import math
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from aoc import Point, Up, Down, Left, Right, Origin, display_points

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

DIRECTIONS = {
  'U': Up,
  'D': Down,
  'L': Left,
  'R': Right,
}

def parse_input(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  dig_plan = []
  for line in lines:
    d, l, c = line.split()
    dig_plan.append((DIRECTIONS[d], int(l)))
  return dig_plan

def get_trench_points(dig_plan):
  points = set()
  point = Origin
  points.add(point)
  for direction, length in dig_plan:
    for _ in range(length):
      point += direction
      points.add(point)
  return points

class Lagoon:
  def __init__(self, file):
    self.dig_plan = parse_input(file)
    self.trench_points = get_trench_points(self.dig_plan)
    self.xmin = min(p.x for p in self.trench_points)
    self.xmax = max(p.x for p in self.trench_points)
    self.ymin = min(p.y for p in self.trench_points)
    self.ymax = max(p.y for p in self.trench_points)
    self.reset()

  def reset(self):
    self.visited = set()
    self.starting_points = set()
    for point in self.trench_points:
      for direction in DIRECTIONS.values():
        if (neighbor := point + direction) not in self.trench_points:
          self.starting_points.add(neighbor)
    self.enclosed_points = set()

  def bfs(self, point):
    current = [point]
    self.visited.add(point)
    pending = set()
    outside = False
    temp_enclosed_points = set()
    temp_enclosed_points.add(point)
    while current:
      for point in current:
        self.starting_points.discard(point)
        for direction in DIRECTIONS.values():
          neighbor = point + direction
          if neighbor in self.visited:
            continue
          if neighbor in self.trench_points:
            continue
          if neighbor.x <= self.xmin or neighbor.x >= self.xmax:
            outside = True
            continue
          if neighbor.y <= self.ymin or neighbor.y >= self.ymax:
            outside = True
            continue
          self.visited.add(neighbor)
          temp_enclosed_points.add(neighbor)
          pending.add(neighbor)
      current = list(pending)
      pending = set()
    if not outside:
      self.enclosed_points |= temp_enclosed_points

  def run(self):
    self.reset()
    while self.starting_points:
      self.bfs(self.starting_points.pop())
    return len(self.trench_points) + len(self.enclosed_points)

DIRECTIONS2 = {
  0: Right,
  1: Down,
  2: Left,
  3: Up,
}

def parse_input2(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  dig_plan = []
  for line in lines:
    _, _, h = line.split()
    direction = DIRECTIONS2[int(h[-2])]
    length = int(h[2:-2], 16)
    dig_plan.append((direction, length))
  return dig_plan

def display_dig_plan(dig_plan):
  current = Origin
  xmin = xmax = ymin = ymax = 0
  segments = []
  for direction, length in dig_plan:
    new = current + direction * length
    segments.append((current, new))
    if new.x < xmin:
      xmin = new.x
    if new.x > xmax:
      xmax = new.x
    if new.y < ymin:
      ymin = new.y
    if new.y > ymax:
      ymax = new.y
    current = new
  fig, ax = plt.subplots()
  ax.set_xlim(xmin, xmax)
  ax.set_ylim(ymin, ymax)
  ax.add_collection(LineCollection(segments))
  plt.show()

def get_segments(dig_plan):
  vertical = []
  horizontal = []
  current = Origin
  for direction, length in dig_plan:
    new = current + direction * length
    if direction in [Up, Down]:
      vertical.append((*sorted(p.y for p in [current, new]), current.x))
    else:
      horizontal.append((*sorted(p.x for p in [current, new]), current.y))
    current = new
  return sorted(vertical), sorted(horizontal)

def get_vertical_ranges(vs):
  pq = []
  for v in vs:
    heapq.heappush(pq, v)
  ranges = []
  active = set()
  tos = {}
  working_range = []
  index = None
  while pq:
    index_from, index_to, column = heapq.heappop(pq)
    if index is None:
      previous = False
      working_range = [index_from + 1]
    else:
      previous = True
    if ((index_to == math.inf and column in active)
        or (previous and index_from > index)):
      working_range.append(index_from - 1)
      working_range.append(tuple(sorted(active)))
      ranges.append(working_range)
      working_range = [index_from + 1]
    done = [col for col, val in tos.items() if val == index_from]
    for d in done:
      active.remove(d)
      del tos[d]
    if index_to != math.inf:
      active.add(column)
      tos[column] = index_to
      heapq.heappush(pq, (index_to, math.inf, column))
    index = index_from
  if index_to != math.inf:
    working_range.append(index_to - 1)
    working_range.append(tuple(sorted(active)))
    ranges.append(working_range)
  return ranges

def scan_line(coords):
  coords = sorted(coords)  # make sure list is sorted
  try:
    return sum(coords[i+1] - coords[i] + 1 for i in range(0, len(coords), 2))
  except IndexError as e:
    print(coords)
    raise e

def scan_range(start, end, coords):
  return (end - start + 1) * scan_line(coords)

def get_horizontals(vs, hs):
  # return [(start, end), (vert1, None), (vert2, None), (start, end)] etc.
  horizontals = collections.defaultdict(list)
  for col_start, col_end, row in hs:
    horizontals[row].append((col_start, col_end))
  for row in horizontals:
    for row_start, row_end, column in vs:
      if row_start < row < row_end:
        horizontals[row].append((column, None))
  return horizontals

def check_inside(column, coords):
  for i in range(0, len(coords), 2):
    if coords[i] < column < coords[i+1]:
      return True
  return False

def get_adjacent_coords(row, vrs):
  return ([r for r in vrs if r[0] == row + 1 or r[1] == row - 1]
          [0]
          [2])

def analyze_horizontal(row, tuples, vrs):
  tuples = sorted(tuples)
  total = 0
  inside = False
  last = None
  for start, end in tuples:
    if inside:
      total += (start - last - 1)  # catches up to just before start
    if end is not None:  # horizontal segment
      total += (end - start + 1)
      inside = check_inside(end + 1, get_adjacent_coords(row, vrs))
      last = end
    else:  # vertical line
      total += 1
      inside = not inside
      last = start
  return total

def get_volume(dig_plan):
  vs, hs = get_segments(dig_plan)
  vrs = get_vertical_ranges(vs)
  horizontals = get_horizontals(vs, hs)
  vrsum = sum(scan_range(*r) for r in vrs)
  hsum = sum(analyze_horizontal(row, tuples, vrs)
             for row, tuples in horizontals.items())
  return vrsum + hsum

test_lagoon = Lagoon(TEST_INPUT_FILE)
assert test_lagoon.run() == 62
test_dig_plan2 = parse_input2(TEST_INPUT_FILE)
assert get_volume(test_dig_plan2) == 952408144115

real_lagoon = Lagoon(INPUT_FILE)
print(f'Day {DAY} part 1: {real_lagoon.run()}')
real_dig_plan2 = parse_input2(INPUT_FILE)
print(f'Day {DAY} part 2: {get_volume(real_dig_plan2)}')
