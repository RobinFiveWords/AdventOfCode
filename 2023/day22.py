import collections
import heapq

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')


def parse_bricks(file):
  with open(file) as f:
    s = f.read()
    assert '-' not in s
    return [Brick(line) for line in s.strip().split('\n')]


P3 = collections.namedtuple('P3', ('x', 'y', 'z'))


class Brick:
  def __init__(self, s):
    self.s = s
    self.points = set()
    self.direction = None
    x0, y0, z0, x1, y1, z1 = parse_ints(s)
    if x0 != x1:
      self.direction = 'x'
      x0, x1 = sorted([x0, x1])
      for x in range(x0, x1 + 1):
        self.points.add(P3(x, y0, z0))
    elif y0 != y1:
      self.direction = 'y'
      y0, y1 = sorted([y0, y1])
      for y in range(y0, y1 + 1):
        self.points.add(P3(x0, y, z0))
    else:
      self.direction = 'z'
      z0, z1 = sorted([z0, z1])
      for z in range(z0, z1 + 1):
        self.points.add(P3(x0, y0, z))
    self.lowest_height = z0
    self.highest_height = z1

    self.can_disintegrate = False

  def copy(self):
    if self.direction == 'x':
      xs = [point.x for point in self.points]
      point = list(self.points)[0]
      y, z = point[1], point[2]
      s = f"{min(xs)},{y},{z}~{max(xs)},{y},{z}"
    elif self.direction == 'y':
      ys = [point.y for point in self.points]
      point = list(self.points)[0]
      x, z = point[0], point[2]
      s = f"{x},{min(ys)},{z}~{x},{max(ys)},{z}"
    else:
      zs = [point.z for point in self.points]
      point = list(self.points)[0]
      x, y = point[0], point[1]
      s = f"{x},{y},{min(zs)}~{x},{y},{max(zs)}"
    return Brick(s)

  def drop(self, distance):
    new_points = set()
    for point in self.points:
      new_points.add(P3(point.x, point.y, point.z - distance))
    self.points = new_points
    self.lowest_height -= distance
    self.highest_height -= distance

  def __lt__(self, other):
    return self.lowest_height < other.lowest_height

  def __repr__(self):
    return f"Brick({self.s} : {self.lowest_height})"


class Snapshot:
  def __init__(self, file, from_existing=None, without_brick=None):
    if from_existing is not None:
      self.bricks = []
      for brick in from_existing.bricks:
        if without_brick is None or without_brick != brick:
          self.bricks.append(brick.copy())
    else:
      self.bricks = parse_bricks(file)
    self.grounded_heights = {}
    self.pq = []
    for brick in self.bricks:
      for point in brick.points:
        self.grounded_heights[(point.x, point.y)] = 0
      heapq.heappush(self.pq, brick)

  def copy(self):
    return Snapshot(None, self)

  def copy_without_brick(self, brick):
    return Snapshot(None, self, brick)

  def smallest_vertical_gap(self, brick):
    return min(point.z - self.grounded_heights[(point.x, point.y)] - 1
               for point in brick.points)

  def drop_one(self):
    if self.pq:
      brick = heapq.heappop(self.pq)
      distance_to_drop = self.smallest_vertical_gap(brick)
      brick.drop(distance_to_drop)
      if brick.direction == 'z':
        point = list(brick.points)[0]
        self.grounded_heights[(point.x, point.y)] = brick.highest_height
      else:
        for point in brick.points:
          self.grounded_heights[(point.x, point.y)] = brick.highest_height
      return distance_to_drop > 0

  def drop_all(self):
    bricks_fallen = 0
    while self.pq:
      result = self.drop_one()
      if result:
        bricks_fallen += 1
    return bricks_fallen

  def containing_bricks(self, points):
    return [brick for brick in self.bricks
            if any(point in points for point in brick.points)]

  def check_disintegrate(self, brick):
    if brick.direction == 'z':
      point = list(brick.points)[0]
      supported_points = [P3(point.x, point.y, brick.highest_height + 1)]
    else:
      supported_points = [P3(point.x, point.y, point.z + 1)
                          for point in brick.points]
    supported_bricks = self.containing_bricks(supported_points)
    brick.supported_bricks = supported_bricks
    if not supported_bricks:
      brick.can_disintegrate = True
      return True
    for sb in supported_bricks:
      if sb.direction == 'z':
        point = list(sb.points)[0]
        supporting_points = [P3(point.x, point.y, sb.lowest_height - 1)]
      else:
        supporting_points = [P3(point.x, point.y, point.z - 1)
                             for point in sb.points]
      supporting_bricks = self.containing_bricks(supporting_points)
      if not any(b is not brick for b in supporting_bricks):
        return False
    brick.can_disintegrate = True
    return True

  def how_many_can_be_disintegrated(self):
    return sum(self.check_disintegrate(brick) for brick in self.bricks)

  def total_fall(self):
    return sum(brick.total_fall() for brick in self.bricks)


def disintegrate_bricks_fallen(snapshot, brick):
  new = snapshot.copy_without_brick(brick)
  return new.drop_all()

def sum_disintegrate_bricks_fallen(snapshot):
  return sum(disintegrate_bricks_fallen(snapshot, brick)
             for brick in snapshot.bricks
             if not brick.can_disintegrate)


test_bricks = Snapshot(TEST_INPUT_FILE)
test_bricks.drop_all()
assert test_bricks.how_many_can_be_disintegrated() == 5
assert sum_disintegrate_bricks_fallen(test_bricks) == 7

real_bricks = Snapshot(INPUT_FILE)
real_bricks.drop_all()
print(f'Day {DAY} part 1: {real_bricks.how_many_can_be_disintegrated()}')
print(f'Day {DAY} part 2: {sum_disintegrate_bricks_fallen(real_bricks)}')



