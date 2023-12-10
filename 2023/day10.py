from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')
TEST_INPUT_FILE2 = INPUT_FILE.replace('input', 'testinput2')
TEST_INPUT_FILE3 = INPUT_FILE.replace('input', 'testinput3')
TEST_INPUT_FILE4 = INPUT_FILE.replace('input', 'testinput4')
TEST_INPUT_FILE5 = INPUT_FILE.replace('input', 'testinput5')
TEST_INPUT_FILE6 = INPUT_FILE.replace('input', 'testinput6')

DIRECTIONS = [Up, Down, Left, Right]

neighbors = {
  '|': [Up, Down],
  '-': [Left, Right],
  'L': [Up, Right],
  'J': [Up, Left],
  '7': [Down, Left],
  'F': [Down, Right],
  '.': [],
}

def parse_input(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  points = {}
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      points[Point(x, y)] = char
  return points

def get_start(points):
  current_points = [p for p, v in points.items() if v == 'S']
  assert len(current_points) == 1
  start = current_points[0]
  next_points = []
  for direction in DIRECTIONS:
    point = start + direction
    for new_direction in neighbors[points.get(point, '.')]:  # ignore out of bounds
      if point + new_direction == start:
        next_points.append(point)
  return current_points, next_points

def get_loop(points):
  current_points, next_points = get_start(points)
  visited = set()
  for start in current_points:
    visited.add(start)
  edges = set()
  steps = 0
  while next_points:
    steps += 1
    current_points = next_points[:]
    next_points = []
    for point in current_points:
      if point not in visited:
        visited.add(point)
        connected = [point + neighbor for neighbor in neighbors[points[point]]]
        for neighbor in connected:
          edges.add((point, neighbor))
          edges.add((neighbor, point))
          if neighbor not in visited:
            next_points.append(neighbor)
  return steps, visited, edges

def double_loop(edges):
  points = set()
  for p1, p2 in edges:
    points.add(p1 * 2)
    points.add(p1 + p2)
    points.add(p2 * 2)
  return points

class BFS:
  def __init__(self, edges):
    self.loop = double_loop(edges)
    self.xmin = min(p.x for p in self.loop)
    self.xmax = max(p.x for p in self.loop)
    self.ymin = min(p.y for p in self.loop)
    self.ymax = max(p.y for p in self.loop)
    self.starting_points = set(Point(x, y)
                               for x in range(self.xmin + 1, self.xmax, 2)
                               for y in range(self.ymin + 1, self.ymax, 2))
    self.visited = set()
    self.enclosed_area = 0

  def bfs(self, point):
    current = [point]
    self.visited.add(point)
    pending = set()
    outside = False
    temp_enclosed_points = set()
    while current:
      for p in current:
        self.starting_points.discard(p)
        for direction in DIRECTIONS:
          neighbor = p + direction
          if neighbor in self.visited:
            continue
          if neighbor in self.loop:
            continue
          if neighbor.x <= self.xmin or neighbor.x >= self.xmax:
            outside = True
            continue
          if neighbor.y <= self.ymin or neighbor.y >= self.ymax:
            outside = True
            continue
          self.visited.add(neighbor)
          if neighbor.x % 2 == 0 and neighbor.y % 2 == 0:
            temp_enclosed_points.add(neighbor)
          pending.add(neighbor)
      current = list(pending)
      pending = set()
    if not outside:
      self.enclosed_area += len(temp_enclosed_points)

  def run(self):
    while self.starting_points:
      self.bfs(self.starting_points.pop())
    return self.enclosed_area

def display(points):
  xmin = min(p.x for p in points)
  xmax = max(p.x for p in points)
  ymin = min(p.y for p in points)
  ymax = max(p.y for p in points)
  for y in range(ymin, ymax + 1):
    for x in range(xmin, xmax + 1):
      if Point(x, y) in points:
        print('#', end='')
      else:
        print(' ', end='')
    print()


test_points = parse_input(TEST_INPUT_FILE)
assert get_loop(test_points)[0] == 4
test_points2 = parse_input(TEST_INPUT_FILE2)
assert get_loop(test_points2)[0] == 8
test_points3 = parse_input(TEST_INPUT_FILE3)
_, _, test_edges3 = get_loop(test_points3)
assert BFS(test_edges3).run() == 4
test_points4 = parse_input(TEST_INPUT_FILE4)
_, _, test_edges4 = get_loop(test_points4)
assert BFS(test_edges4).run() == 4
test_points5 = parse_input(TEST_INPUT_FILE5)
_, _, test_edges5 = get_loop(test_points5)
assert BFS(test_edges5).run() == 8
test_points6 = parse_input(TEST_INPUT_FILE6)
_, _, test_edges6 = get_loop(test_points6)
assert BFS(test_edges6).run() == 10

real_points = parse_input(INPUT_FILE)
real_steps, real_nodes, real_edges = get_loop(real_points)
print(f'Day {DAY} part 1: {real_steps}')
print(f'Day {DAY} part 2: {BFS(real_edges).run()}')
