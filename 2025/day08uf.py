from aoc import parse_ints, Point3


def parse_file(file):
  with open(file) as f:
    return [Point3(*parse_ints(line)) for line in f.read().strip().split('\n')]


def euclidean_squared(p1, p2):
  return (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2


def get_distances(points):
  return sorted((euclidean_squared(p1, p2), i, j)
                for i, p1 in enumerate(points[:-1])
                for j, p2 in enumerate(points[i+1:], start=i+1))


class UnionFind:
  def __init__(self, n):
    self.parent = list(range(n))
    self.size = [1] * n
    self.count = n

  def find(self, i):
    while i != self.parent[i]:
      self.parent[i] = self.parent[self.parent[i]]
      i = self.parent[i]
    return i

  def union(self, p, q):
    root_p = self.find(p)
    root_q = self.find(q)

    if root_p == root_q:
      return False

    if self.size[root_p] < self.size[root_q]:
      self.parent[root_p] = root_q
      self.size[root_q] += self.size[root_p]
    else:
      self.parent[root_q] = root_p
      self.size[root_p] += self.size[root_q]

    self.count -= 1
    return True


class Connect:
  def __init__(self, file):
    self.points = parse_file(file)
    self.distances = get_distances(self.points)
    self.uf = UnionFind(len(self.points))

  def run(self):
    for _, i, j in self.distances:
      self.uf.union(i, j)
      if self.uf.count == 1:
        break
    return self.points[i].x * self.points[j].x


assert Connect('testinput08.txt').run() == 25272

print('Day 8 part 2:', Connect('input08.txt').run())
