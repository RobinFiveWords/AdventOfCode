from collections import Counter
from fractions import Fraction
from sympy import Matrix, solve_linear_system
from sympy.abc import t, u, v

from aoc import parse_ints, Point

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

MINXY = 200000000000000
MAXXY = 400000000000000


def parse_file(file):
  with open(file) as f:
    rows = [parse_ints(line, True) for line in f.read().strip().split('\n')]
  # check that no paths are aligned with x or y axis
  assert not any(row[3] == 0 or row[4] == 0 for row in rows)
  return rows


class Hailstone:
  def __init__(self, row, minxy, maxxy):
    self.px, self.py, self.pz, self.vx, self.vy, self.vz = row
    self.slope_yx = Fraction(self.vy, self.vx)
    self.segment = self.intersections_test_area(minxy, maxxy)
    self.direction = (int(self.vx > 0) 
                      + 2 * int(self.vy > 0)
                      + 4 * int(self.vz > 0))
    self.magnitude = sum(map(lambda n: n ** 2, [self.vx, self.vy, self.vz]))

  def intersect_x(self, y0):
    return self.px - ((self.py - y0) / self.slope_yx)

  def intersect_y(self, x0):
    return self.py - (self.slope_yx * (self.px - x0))

  def intersections_test_area(self, minxy, maxxy):
    points = [Point(minxy, self.intersect_y(minxy)),
              Point(maxxy, self.intersect_y(maxxy)),
              Point(self.intersect_x(minxy), minxy),
              Point(self.intersect_x(maxxy), maxxy)]
    return [p for p in points
            if minxy <= p.x <= maxxy
            and minxy <= p.y <= maxxy]

  def time_x(self, x0):
    return (x0 - self.px) / self.vx


def cross2D(v1, v2):
  return v1.x * v2.y - v1.y * v2.x

def intersection2Dsegments(segment1, segment2):
  """Adapted from https://stackoverflow.com/a/565282/5017927."""
  if len(segment1) == 0 or len(segment2) == 0:
    return None
  p = segment1[0]
  q = segment2[0]
  r = segment1[1] - p
  s = segment2[1] - q
  t_numerator = cross2D(q - p, s)
  u_numerator = cross2D(q - p, r)
  denominator = cross2D(r, s)
  if denominator == 0:
    assert not u_numerator == 0, 'Collinear case not managed'
    return None  # parallel and non-intersecting
  t = Fraction(t_numerator, denominator)
  u = Fraction(u_numerator, denominator)
  if 0 <= t <= 1 and 0 <= u <= 1:
    return p + r * t
  return None

def intersection2Dforward(h1, h2):
  intersection = intersection2Dsegments(h1.segment, h2.segment)
  if intersection is None:
    return False
  return h1.time_x(intersection.x) > 0 and h2.time_x(intersection.x) > 0

def total_intersections_2D_forward(hailstones):
  return sum(intersection2Dforward(hailstones[i], hailstones[j])
             for i in range(len(hailstones) - 1)
             for j in range(i + 1, len(hailstones)))

test_hailstones = [Hailstone(r, 7, 27) for r in parse_file(TEST_INPUT_FILE)]
assert total_intersections_2D_forward(test_hailstones) == 2

real_hailstones = [Hailstone(r, MINXY, MAXXY) for r in parse_file(INPUT_FILE)]
print(f'Day {DAY} part 1: {total_intersections_2D_forward(real_hailstones)}')


# for part 2, we'll find three points that are drifting at the same speed
# in one of the three dimensions, let's choose the x dimension,
# reducing the problem to two dimensions
# where the spacing in time of crossing lines 1, 2, 3
# is proportional to the difference in x position of lines 1, 2, 3

vx_counts = Counter(h.vx for h in real_hailstones)
vx3s = [v for v, count in vx_counts.items() if count == 3]
vx = vx3s[-1]
h1, h2, h3 = sorted((h for h in real_hailstones if h.vx == vx), key=lambda h: h.px)

F = Fraction(h2.px - h1.px, h3.px - h1.px)

def new_position(h, t):
  new_x = h.px + t * h.vx
  new_y = h.py + t * h.vy
  new_z = h.pz + t * h.vz
  return (new_x, new_y, new_z)

# F also equals (t2 - t1) / (t3 - t1)
# and this also equals,
# for each of y and z,

# (new_position(h2, t2) - new_posiiton(h1, t1))
# divided by 
# (new_position(h3, t3) - new_position(h1, t1))

# so we have three linear equations in the variables t1, t2, t3

# a bunch of algebra to arrive at these coefficients:
c00 = F - 1
c01 = 1
c02 = -F
c03 = 0
c10 = (F - 1) * h1.vy
c11 = h2.vy
c12 = -F * h3.vy
c13 = h1.py - h2.py + F * h3.py - F * h1.py
c20 = (F - 1) * h1.vz
c21 = h2.vz
c22 = -F * h3.vz
c23 = h1.pz - h2.pz + F * h3.pz - F * h1.pz

m = Matrix(((c00, c01, c02, c03),
            (c10, c11, c12, c13),
            (c20, c21, c22, c23)))
results = solve_linear_system(m, t, u, v)
t1, t2, t3 = results[t], results[u], results[v]

if t1 < t2:
  x1, y1, z1 = new_position(h1, t1)
  x2, y2, z2 = new_position(h2, t2)
  scaled_t = t2 / (t2 - t1)
else:
  x1, y1, z1 = new_position(h2, t2)
  x2, y2, z2 = new_position(h1, t1)
  scaled_t = t1 / (t1 - t2)

x0 = x2 - (x2 - x1) * scaled_t
y0 = y2 - (y2 - y1) * scaled_t
z0 = z2 - (z2 - z1) * scaled_t

print(f'Day {DAY} part 2: {x0 + y0 + z0}')
