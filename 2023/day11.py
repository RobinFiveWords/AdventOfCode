from aoc import Point

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

def parse_input(file, expansion=2):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  assert 1 == len(set(len(line) for line in lines))
  xs = set(range(len(lines[0])))
  ys = set(range(len(lines)))
  initial_points = []
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == '#':
        xs.discard(x)
        ys.discard(y)
        initial_points.append(Point(x, y))
  resulting_points = []
  for point in initial_points:
    resulting_x = point.x + (expansion - 1) * sum(x < point.x for x in xs)
    resulting_y = point.y + (expansion - 1) * sum(y < point.y for y in ys)
    resulting_points.append(Point(resulting_x, resulting_y))
  return resulting_points

def shortest_paths(points):
  return sum(points[i].manhattan_distance(points[j])
             for i in range(len(points) - 1)
             for j in range(i + 1, len(points)))

assert shortest_paths(parse_input(TEST_INPUT_FILE)) == 374
assert shortest_paths(parse_input(TEST_INPUT_FILE, 10)) == 1030
assert shortest_paths(parse_input(TEST_INPUT_FILE, 100)) == 8410

real_points = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {shortest_paths(real_points)}')
real_points2 = parse_input(INPUT_FILE, 1_000_000)
print(f'Day {DAY} part 2: {shortest_paths(real_points2)}')
