from collections import Counter
from math import prod

from aoc import parse_ints, sign, Point, display_points

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

XMOD = 101
YMOD = 103

def parse_input(file):
  with open(file) as f:
    return [parse_ints(line, True) for line in f.read().strip().split('\n')]

def move_robot(robot, seconds, xmod, ymod):
  px, py, vx, vy = robot
  ox = (px + seconds * vx) % xmod
  oy = (py + seconds * vy) % ymod
  return ox, oy, vx, vy

def safety_factor(robots, xmod, ymod):
  xmid = xmod // 2
  ymid = ymod // 2
  c = Counter()
  for robot in robots:
    xq = sign(robot[0] - xmid)
    yq = sign(robot[1] - ymid)
    c[(xq, yq)] += 1
  return prod(v for (xq, yq), v in c.items()
              if xq in [-1, 1] and yq in [-1, 1])

def observe(robots, seconds, xmod, ymod):
  robots = [move_robot(robot, seconds, xmod, ymod) for robot in robots]
  return safety_factor(robots, xmod, ymod)

def display(robots):
  points = Counter(Point(*robot[:2]) for robot in robots)
  xmax = max(p.x for p in points)
  ymax = max(p.y for p in points)
  for y in range(ymax + 1):
    for x in range(xmax + 1):
      quantity = points.get(Point(x, y), 0)
      if quantity == 0:
        print('.', end='')
      elif quantity > 9:
        print('#', end='')
      else:
        print(str(quantity), end='')
    print()

class Robots:
  def __init__(self, file, xmod, ymod):
    self.robots = parse_input(file)
    self.xmod = xmod
    self.ymod = ymod
    self.seconds = 0
    self.xmid = self.xmod // 2
    self.ymid = self.ymod // 2
    self.safety_factors = [self.safety_factor()]

  def cycle(self, verbose=False):
    self.seconds += 1
    for robot in self.robots:
      robot[0] = (robot[0] + robot[2]) % self.xmod
      robot[1] = (robot[1] + robot[3]) % self.ymod
    self.safety_factors.append(self.safety_factor())
    if verbose:
      print(f"{self.seconds:>8} {self.safety_factor():>9}")

  def safety_factor(self):
    c = Counter()
    for robot in self.robots:
      xq = sign(robot[0] - self.xmid)
      yq = sign(robot[1] - self.ymid)
      c[(xq, yq)] += 1
    return prod(v for (xq, yq), v in c.items()
                if xq in [-1, 1] and yq in [-1, 1])

  def display(self):
    points = Counter(Point(*robot[:2]) for robot in self.robots)
    xmax = max(p.x for p in points)
    ymax = max(p.y for p in points)
    for y in range(ymax + 1):
      for x in range(xmax + 1):
        quantity = points.get(Point(x, y), 0)
        if quantity == 0:
          print('.', end='')
        elif quantity > 9:
          print('#', end='')
        else:
          print(str(quantity), end='')
      print()

def main():
  print(f'Day {DAY} part 1: {observe(parse_input(INPUT_FILE), 100, XMOD, YMOD)}')
  R = Robots(INPUT_FILE, XMOD, YMOD)
  for _ in range(10000):
    R.cycle()
  print(f'Day {DAY} part 2: {R.safety_factors.index(min(R.safety_factors))}')
  pass

# guessed that the Easter egg would have an extreme safety factor,
# then simulated and displayed a few of the results until it popped out

if __name__ == '__main__':
  main()
