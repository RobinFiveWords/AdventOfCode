from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Down, Left, Right]

class Map:
  def __init__(self, file):
    self.points = {}
    self.trailheads = []
    with open(file) as f:
      lines = f.read().strip().split('\n')
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        point = Point(x, y)
        height = int(char)
        self.points[point] = height
        if height == 0:
          self.trailheads.append(point)

  def score(self, trailhead):
    assert self.points[trailhead] == 0
    result = 0
    height = 0
    current = [trailhead]
    pending = set()
    while current:
      for point in current:
        if height == 9:
          result += 1
          continue
        for direction in DIRECTIONS:
          neighbor = point + direction
          next_height = self.points.get(neighbor, 0)
          if next_height - 1 == height:
            pending.add(neighbor)
      height += 1
      current = list(pending)
      pending = set()
    return result

  def total_score(self):
    return sum(self.score(trailhead) for trailhead in self.trailheads)

  def dfs(self, current):
    height = self.points[current]
    if height == 9:
      return 1
    result = 0
    for direction in DIRECTIONS:
      neighbor = current + direction
      next_height = self.points.get(neighbor, 0)
      if next_height - 1 == height:
        result += self.dfs(neighbor)
    return result

  def total_score2(self):
    return sum(self.dfs(trailhead) for trailhead in self.trailheads)

def main():
  print(f'Day {DAY} part 1: {Map(INPUT_FILE).total_score()}')
  print(f'Day {DAY} part 2: {Map(INPUT_FILE).total_score2()}')
  pass

if __name__ == '__main__':
  main()
