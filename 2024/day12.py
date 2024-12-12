from collections import defaultdict

from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Down, Left, Right]

def parse_input(file):
  points = {}
  with open(file) as f:
    for y, line in enumerate(f.read().strip().split('\n')):
      for x, char in enumerate(line):
        points[Point(x, y)] = char
  return points


class Component:
  def __init__(self, points, label):
    self.points = points
    self.label = label
    self.adj = {point: set() for point in self.points}
    for p1 in self.points:
      for p2 in self.points:
        if p1 == p2:
          continue
        for direction in DIRECTIONS:
          if p1 + direction == p2:
            self.adj[p1].add(p2)
            self.adj[p2].add(p1)
    self.by_row = defaultdict(list)
    self.by_col = defaultdict(list)
    for point in self.points:
      self.by_row[point.y].append(point)
      self.by_col[point.x].append(point)

  def __repr__(self):
    return f"Component({self.points}, '{self.label}')"

  def price(self):
    return sum(4 - len(v) for v in self.adj.values()) * len(self.points)

  def price2(self):
    # sweep rows and sweep columns
    # in each row, count intervals where there is no top neighbor
    # and count intervals where there is no bottom neighbor
    # in each column, count intervals where there is no left neighbor
    # and count intervals where there is no right neighbor
    xmin = min(p.x for p in self.points)
    xmax = max(p.x for p in self.points)
    ymin = min(p.y for p in self.points)
    ymax = max(p.y for p in self.points)

    horizontal_sides = 0
    for y in range(ymin, ymax + 1):
      no_top_neighbor = []
      no_bottom_neighbor = []
      for x in range(xmin, xmax + 1):
        point = Point(x, y)
        if point not in self.points:
          continue
        if point + Up not in self.points:
          no_top_neighbor.append(x)
        if point + Down not in self.points:
          no_bottom_neighbor.append(x)
      if no_top_neighbor:
        horizontal_sides += 1
        horizontal_sides += sum(1 for i in range(len(no_top_neighbor) - 1)
                                if no_top_neighbor[i] + 1 < no_top_neighbor[i+1])
      if no_bottom_neighbor:
        horizontal_sides += 1
        horizontal_sides += sum(1 for i in range(len(no_bottom_neighbor) - 1)
                                if no_bottom_neighbor[i] + 1 < no_bottom_neighbor[i+1])

    vertical_sides = 0
    for x in range(xmin, xmax + 1):
      no_left_neighbor = []
      no_right_neighbor = []
      for y in range(ymin, ymax + 1):
        point = Point(x, y)
        if point not in self.points:
          continue
        if point + Left not in self.points:
          no_left_neighbor.append(y)
        if point + Right not in self.points:
          no_right_neighbor.append(y)
      if no_left_neighbor:
        vertical_sides += 1
        vertical_sides += sum(1 for i in range(len(no_left_neighbor) - 1)
                              if no_left_neighbor[i] + 1 < no_left_neighbor[i+1])
      if no_right_neighbor:
        vertical_sides += 1
        vertical_sides += sum(1 for i in range(len(no_right_neighbor) - 1)
                              if no_right_neighbor[i] + 1 < no_right_neighbor[i+1])

    return (horizontal_sides + vertical_sides) * len(self.points)


class Garden:
  def __init__(self, file):
    self.points = parse_input(file)
    self.components = []
    self.bfs_components()

  def bfs_components(self):
    assert not self.components
    working = set(self.points)
    while working:
      start = working.pop()
      label = self.points[start]
      current = [start]
      points = set(current)
      visited = points.copy()
      pending = set()
      while current:
        for point in current:
          for direction in DIRECTIONS:
            neighbor = point + direction
            if neighbor in visited:
              continue
            if self.points.get(neighbor, None) == label:
              working.remove(neighbor)
              points.add(neighbor)
              pending.add(neighbor)
              visited.add(neighbor)
        current = list(pending)
        pending = set()
      self.components.append(Component(points, label))

  def total_price(self):
    return sum(component.price() for component in self.components)

  def total_price2(self):
    return sum(component.price2() for component in self.components)


def main():
  g = Garden(INPUT_FILE)
  print(f'Day {DAY} part 1: {g.total_price()}')
  print(f'Day {DAY} part 2: {g.total_price2()}')
  pass

if __name__ == '__main__':
  main()
