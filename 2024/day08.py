from collections import defaultdict
from fractions import Fraction

from aoc import Point

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

class Map:
  def __init__(self, file):
    self.antennas = defaultdict(list)
    with open(file) as f:
      lines = f.read().strip().split('\n')
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        if char == '.':
          continue
        self.antennas[char].append(Point(x, y))
    self.xmax = x
    self.ymax = y
    self.antinodes = set()
    for char in self.antennas:
      antennas = self.antennas[char]
      for i in range(len(antennas) - 1):
        for j in range(i + 1, len(antennas)):
          pi = antennas[i]
          pj = antennas[j]
          diff = pj - pi
          self.antinodes.add(pi - diff)
          self.antinodes.add(pj + diff)
    self.antinodes2 = set()
    for char, antennas in self.antennas.items():
      assert len(antennas) == len(set(p.x for p in antennas)), f"'{char}' has vertical line"
      for i, pi in enumerate(antennas[:-1]):
        for pj in antennas[i + 1:]:
          diff = pj - pi
          dy, dx = Fraction(diff.y, diff.x).as_integer_ratio()  # dx is always positive
          n = pi.x // dx  # antinodes left of pi
          step = Point(dx, dy)
          current = pi - (step * n)
          while 0 <= current.x <= self.xmax:
            self.antinodes2.add(current)
            current += step

  def within_bounds(self):
    return sum(1 for p in self.antinodes
               if 0 <= p.x <= self.xmax
               and 0 <= p.y <= self.ymax)

  def within_bounds2(self):
    return sum(1 for p in self.antinodes2
               if 0 <= p.x <= self.xmax
               and 0 <= p.y <= self.ymax)

def main():
  print(f'Day {DAY} part 1: {Map(INPUT_FILE).within_bounds()}')
  print(f'Day {DAY} part 2: {Map(INPUT_FILE).within_bounds2()}')
  pass

if __name__ == '__main__':
  main()
