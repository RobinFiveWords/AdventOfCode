from aoc import Point, Up, Down, Left, Right

NEIGHBORS8 = [Up, Down, Left, Right,
              Up + Left, Up + Right, Down + Left, Down + Right]


def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  points = set()
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == '@':
        points.add(Point(x, y))
  return points


def accessible(p, points):
  return sum(1 for neighbor in NEIGHBORS8 if p + neighbor in points) < 4


def points_accessible(points):
  return sum(accessible(p, points) for p in points)

assert points_accessible(parse_file('testinput04.txt')) == 13


def remove(points):
  start = len(points)
  working = points.copy()
  while (removable := [p for p in working if accessible(p, working)]):
    for p in removable:
      working.remove(p)
  return start - len(working)

assert remove(parse_file('testinput04.txt')) == 43


print('Day 4 part 1:', points_accessible(parse_file('input04.txt')))
print('Day 4 part 2:', remove(parse_file('input04.txt')))
