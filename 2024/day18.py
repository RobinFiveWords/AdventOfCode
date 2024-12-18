from aoc import parse_ints, Point, Up, Down, Left, Right, Origin

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Down, Left, Right]

REAL_EXIT = Point(70, 70)

class Space:
  def __init__(self, file, exit):
    with open(file) as f:
      self.walls = [Point(*parse_ints(line))
                   for line in f.read().strip().split('\n')]
    self.start = Origin
    self.xmin, self.ymin = self.start
    self.exit = exit
    self.xmax, self.ymax = self.exit

  def shortest(self, number_of_walls):
    walls = set(self.walls[:number_of_walls])
    current = [self.start]
    visited = set(current)
    pending = set()
    steps = 0
    while current:
      steps += 1
      for point in current:
        for direction in DIRECTIONS:
          neighbor = point + direction
          if neighbor == self.exit:
            return steps
          if neighbor in visited or neighbor in walls:
            continue
          if neighbor.x < self.xmin or neighbor.x > self.xmax or neighbor.y < self.ymin or neighbor.y > self.ymax:
            continue
          visited.add(neighbor)
          pending.add(neighbor)
      current = list(pending)
      pending = set()

  def search(self, start):
    minimum = 0
    maximum = len(self.walls)
    assert minimum <= start <= maximum
    candidate = start
    while minimum < maximum:
      result = self.shortest(candidate)
      if result is None:
        maximum = candidate - 1
        candidate = (minimum + maximum) // 2
      else:
        minimum = candidate
        candidate = max(minimum + 1, (minimum + maximum) // 2)
    critical_point = self.walls[minimum]
    return ','.join(map(str, critical_point))


def main():
  print(f'Day {DAY} part 1: {Space(INPUT_FILE, REAL_EXIT).shortest(1024)}')
  print(f'Day {DAY} part 2: {Space(INPUT_FILE, REAL_EXIT).search(1024)}')
  pass

if __name__ == '__main__':
  main()
