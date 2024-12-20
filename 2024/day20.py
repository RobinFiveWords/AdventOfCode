from collections import Counter

from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Down, Left, Right]


class Maze:
  def __init__(self, file):
    with open(file) as f:
      lines = f.read().strip().split('\n')
    self.points = set()
    self.start = None
    self.end = None
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        point = Point(x, y)
        if char == '#':
          continue
        self.points.add(point)
        if char == 'S':
          self.start = point
        elif char == 'E':
          self.end = point
    self.xmax = x
    self.ymax = y
    self.track_index = {}
    self.set_track_index()
    self.cheats = {}
    self.find_cheats()
    self.cheat_counts = Counter(self.cheats.values())
    self.cheats2 = {}
    self.find_cheats2()
    self.cheat_counts2 = Counter(self.cheats2.values())

  def set_track_index(self):
    current = self.start
    index = 0
    self.track_index[current] = index
    while current != self.end:
      index += 1
      neighbors = [current + direction for direction in DIRECTIONS]
      for neighbor in neighbors:
        if neighbor in self.track_index:
          continue
        if neighbor not in self.points:
          continue
        current = neighbor
      self.track_index[current] = index

  def find_cheats(self):
    for y in range(1, self.ymax):
      for x in range(1, self.xmax):
        p1 = Point(x, y)
        if p1 not in self.points:
          continue
        for direction in [Down, Right]:
          p2 = p1 + direction + direction
          if p2 not in self.points:
            continue
          o1, o2 = sorted([p1, p2], key=lambda p: self.track_index[p])
          saved = self.track_index[o2] - self.track_index[o1] - 2
          self.cheats[(o1, o2)] = saved

  def count_cheats(self, n):
    return sum(1 for v in self.cheats.values() if v >= n)

  def find_cheats2(self):
    for y1 in range(1, self.ymax):
      for x1 in range(1, self.xmax):
        p1 = Point(x1, y1)
        if p1 not in self.points:
          continue
        for y2 in range(y1 - 20, y1 + 21):
          if y2 < 1 or y2 > self.ymax:
            continue
          y_dist = abs(y2 - y1)
          x_width = 20 - y_dist
          for x2 in range(x1 - x_width, x1 + x_width + 1):
            if x2 < 1 or x2 > self.xmax:
              continue
            p2 = Point(x2, y2)
            if p2 not in self.points:
              continue
            i1 = self.track_index[p1]
            i2 = self.track_index[p2]
            if i1 > i2:
              continue
            if (p1, p2) in self.cheats2:
              continue
            saved = i2 - i1 - p1.manhattan_distance(p2)
            if p2 == self.end:
              self.cheats2[(p1, p2)] = saved
              continue
            self.cheats2[(p1, p2)] = saved

  def count_cheats2(self, n):
    return sum(1 for v in self.cheats2.values() if v >= n)


def main():
  m = Maze(INPUT_FILE)
  print(f'Day {DAY} part 1: {m.count_cheats(100)}')
  print(f'Day {DAY} part 2: {m.count_cheats2(100)}')
  pass

if __name__ == '__main__':
  main()
