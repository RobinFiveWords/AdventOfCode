from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

changes = {
  (Up   , '/' ): [Right],
  (Up   , '\\'): [Left],
  (Up   , '|' ): [Up],
  (Up   , '-' ): [Left, Right],
  (Down , '/' ): [Left],
  (Down , '\\'): [Right],
  (Down , '|' ): [Down],
  (Down , '-' ): [Left, Right],
  (Left , '/' ): [Down],
  (Left , '\\'): [Up],
  (Left , '|' ): [Up, Down],
  (Left , '-' ): [Left],
  (Right, '/' ): [Up],
  (Right, '\\'): [Down],
  (Right, '|' ): [Up, Down],
  (Right, '-' ): [Right],
}

def parse_input(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  xmax = len(lines[0]) - 1
  ymax = len(lines) - 1
  objs = {}
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char != '.':
        objs[Point(x, y)] = char
  return objs, xmax, ymax

def energized_points(objs, xmax, ymax, start=(Point(-1, 0), Right)):
  current = [start]
  pending = set()
  seen = set()
  seen.add(start)
  energized = set()

  while current:
    for point, direction in current:
      next_point = point + direction
      if not (0 <= next_point.x <= xmax and 0 <= next_point.y <= ymax):
        continue
      energized.add(next_point)
      next_obj = objs.get(next_point, None)
      next_directions = changes.get((direction, next_obj), [direction])
      for next_direction in next_directions:
        next_candidate = (next_point, next_direction)
        if next_candidate in seen:
          continue
        seen.add(next_candidate)
        pending.add(next_candidate)
    current = list(pending)
    pending = set()
  return len(energized)

def max_energized(objs, xmax, ymax):
  candidates = []
  for x in range(xmax + 1):
    candidates.append((Point(x, -1), Down))
    candidates.append((Point(x, ymax + 1), Up))
  for y in range(ymax + 1):
    candidates.append((Point(-1, y), Right))
    candidates.append((Point(xmax + 1, y), Left))
  return max(energized_points(objs, xmax, ymax, candidate)
             for candidate in candidates)

test_objs, test_xmax, test_ymax = parse_input(TEST_INPUT_FILE)
assert energized_points(test_objs, test_xmax, test_ymax) == 46
assert max_energized(test_objs, test_xmax, test_ymax) == 51

real_objs, real_xmax, real_ymax = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {energized_points(real_objs, real_xmax, real_ymax)}')
print(f'Day {DAY} part 2: {max_energized(real_objs, real_xmax, real_ymax)}')
