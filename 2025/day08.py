from collections import defaultdict
from copy import deepcopy
import math

from aoc import parse_ints, Point3


def parse_file(file):
  with open(file) as f:
    return sorted(Point3(*parse_ints(line))
                  for line in f.read().strip().split('\n'))


def closest(points):
  best_points = []
  best = float('inf')
  for i, p1 in enumerate(points[:-1]):
    for p2 in points[i+1:]:
      distance = p1.euclidean_distance_squared(p2)
      if distance < best:
        best_points = [(p1, p2)]
        best = distance
      elif distance == best:
        best_points.append((p1, p2))
  return best_points


def get_distances(points):
  # assuming all distances are unique
  return sorted((p1.euclidean_distance_squared(p2), p1, p2)
                for i, p1 in enumerate(points[:-1])
                for p2 in (points[i+1:]))


def make_N_connections(points, N):
  distances = get_distances(points)
  adj = defaultdict(set)
  for _, p1, p2 in distances[:N]:
    adj[p1].add(p2)
    adj[p2].add(p1)
  components = []
  working = list(adj.keys())
  in_progress = set()
  current = []
  while working:
    in_progress.add(working.pop())
    current = list(in_progress)
    previous = []
    while current:
      previous = current[:]
      current.clear()
      for candidate in working:
        if any(candidate in adj[point] for point in previous):
          current.append(candidate)
          working.remove(candidate)
      in_progress.update(current)
    components.append(list(in_progress))
    in_progress.clear()
  return components


def prod_largest_N_sizes(components, N=3):
  sizes = sorted(len(c) for c in components)
  return math.prod(sizes[-N:])


class Search:
  def __init__(self, file):
    self.points = parse_file(file)
    self.distances = get_distances(self.points)
    self.adj = defaultdict(set)

  def add_connection(self, n):
    _, p1, p2 = self.distances[n]
    self.adj[p1].add(p2)
    self.adj[p2].add(p1)

  def check_all_in_adj(self):
    return len(self.adj.keys()) == len(self.points)

  def check_all_connected(self):
    working = list(self.adj.keys())
    first_point = working.pop()
    current = [first_point]
    in_progress = set(current)
    previous = []
    while current:
      previous = current[:]
      current.clear()
      for candidate in working:
        if any(candidate in self.adj[point] for point in in_progress):
          current.append(candidate)
          working.remove(candidate)
      in_progress.update(current)
    return not working

  def run(self):
    n = 0
    while not self.check_all_in_adj():
      self.add_connection(n)
      n += 1
    lo = n - 1
    if self.check_all_connected():
      return self.answer(lo)
    hi = len(self.distances)
    while lo + 1 < hi:
      previous_adj = deepcopy(self.adj)
      mid = (lo + hi) // 2
      for n in range(lo, mid + 1):
        self.add_connection(n)
      if self.check_all_connected():
        hi = mid
        self.adj = previous_adj
      else:
        lo = mid
    return self.answer(hi)

  def answer(self, n):
    _, p1, p2 = self.distances[n]
    return p1.x * p2.x


test_points = parse_file('testinput08.txt')
test_components = make_N_connections(test_points, 10)
assert prod_largest_N_sizes(test_components) == 40

test_search = Search('testinput08.txt')
assert test_search.run() == 25272

real_points = parse_file('input08.txt')
real_components = make_N_connections(real_points, 1000)

real_search = Search('input08.txt')

print('Day 8 part 1:', prod_largest_N_sizes(real_components))
print('Day 8 part 2:', real_search.run())
