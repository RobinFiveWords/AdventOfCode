import collections
import itertools
from pprint import pprint

from aoc import Point, Up, Down, Left, Right, flatten

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

DIRECTIONS = [Up, Down, Left, Right]

def get_points(lines):
  points = {}
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == '#':
        continue
      points[Point(x, y)] = char
  return points

def get_adjacency_list(points):
  adj = collections.defaultdict(set)
  for p in points:
    for direction in DIRECTIONS:
      if (neighbor := p + direction) in points:
        adj[p].add(neighbor)
        adj[neighbor].add(p)
  return adj

def get_adj_component(points):
  adj = collections.defaultdict(set)
  for p, char in points.items():
    if char != '.':
      continue
    for direction in DIRECTIONS:
      neighbor = p + direction
      if neighbor in points and points[neighbor] == '.':
        adj[p].add(neighbor)
        adj[neighbor].add(p)
  return adj


class Graph:
  def __init__(self, file, slopes_normal=False):
    with open(file) as f:
      self.points = get_points(f.read().strip().split('\n'))
    self.adj = get_adjacency_list(self.points)
    self.adjc = get_adj_component(self.points)
    self.components = {p: None for p in self.adjc}
    self.get_connected_components()
    self.component_lengths = collections.Counter(self.components.values())
    self.segments = collections.defaultdict(set)
    self.get_segments()
    self.digraph_edges = []
    if slopes_normal:
      self.get_digraph_edges_slopes_normal()
    else:
      self.get_digraph_edges()
    self.digraph_nodes = set(itertools.chain.from_iterable(
        edge[:2] for edge in self.digraph_edges))

  def get_connected_components(self):
    component = 0
    while None in self.components.values():
      remaining = [p for p, v in self.components.items() if v is None]
      point = remaining[0]
      self.dfs_component(point, component)
      component += 1

  def dfs_component(self, point, component):
    self.components[point] = component
    for next_point in self.adjc[point]:
      if self.components[next_point] is None:
        self.dfs_component(next_point, component)

  def get_segments(self):
    for point, component in self.components.items():
      if len(self.adjc[point]) == 1:
        self.segments[component].add(point)

  def get_digraph_edges(self):
    for component, segment in self.segments.items():
      p1, p2 = sorted(segment)
      self.digraph_edges.append((p1, p2, self.component_lengths[component] - 1))
      self.digraph_edges.append((p2, p1, self.component_lengths[component] - 1))
    for point, char in self.points.items():
      if char == '.':
        continue
      if char == '>':
        self.digraph_edges.append((point + Left, point + Right, 2))
      elif char == 'v':
        self.digraph_edges.append((point + Up, point + Down, 2))
      else:
        raise ValueError(f"Unexpected character {char}")

  def get_digraph_edges_slopes_normal(self):
    extensions = collections.defaultdict(list)
    for point, char in self.points.items():
      if char == '.':
        continue
      if char == '>':
        p1, p2 = point + Left, point + Right
        extensions[p1].append(p2)
        extensions[p2].append(p1)
      elif char == 'v':
        p1, p2 = point + Up, point + Down
        extensions[p1].append(p2)
        extensions[p2].append(p1)
      else:
        raise ValueError(f"Unexpected character {char}")
    for component, segment in self.segments.items():
      p1, p2 = sorted(segment)
      length = self.component_lengths[component] - 1
      if p1 in extensions:
        ext = extensions[p1]
        assert len(ext) == 1
        p1 = ext[0]
        length += 2
      if p2 in extensions:
        ext = extensions[p2]
        assert len(ext) == 1
        p2 = ext[0]
        length += 2
      self.digraph_edges.append((p1, p2, length))
      self.digraph_edges.append((p2, p1, length))


def get_endpoints(graph):
  ymin = min(p.y for p in graph.points)
  ymax = max(p.y for p in graph.points)
  start = [p for p in graph.points if p.y == ymin]
  assert len(start) == 1
  end = [p for p in graph.points if p.y == ymax]
  assert len(end) == 1
  return (start[0], end[0])


class DiGraph:
  def __init__(self, graph):
    self.start, self.end = get_endpoints(graph)
    self.es = graph.digraph_edges[:]
    self.vs = set(graph.digraph_nodes)
    self.adj = collections.defaultdict(dict)
    for p1, p2, weight in self.es:
      self.adj[p1][p2] = weight
    self.state_bitmask = {v: 1 << i for i, v in enumerate(self.vs)}

  def find_path_lengths(self):
    path_lengths = collections.Counter()
    # state format (visited bitmask, current vertex, steps walked)
    state = (self.state_bitmask[self.start], self.start)
    steps = 0
    current = [(state, steps)]
    pending = {}
    while current:
      for (bitmask, vertex), steps in current:
        for next_vertex, weight in self.adj[vertex].items():
          next_bit = self.state_bitmask[next_vertex]
          if next_bit & bitmask:
            continue
          next_steps = steps + weight
          if next_vertex == self.end:
            path_lengths[next_steps] += 1
            continue
          next_bitmask = next_bit | bitmask
          next_state = (next_bitmask, next_vertex)
          previous_most_steps = pending.get(next_state, 0)
          if next_steps > previous_most_steps:
            pending[next_state] = next_steps
      current = list(pending.items())
      pending = {}
    return path_lengths


test_graph = Graph(TEST_INPUT_FILE)
test_digraph = DiGraph(test_graph)
test_path_lengths = test_digraph.find_path_lengths()
assert max(test_path_lengths) == 94
test_graph2 = Graph(TEST_INPUT_FILE, True)
test_digraph2 = DiGraph(test_graph2)
test_path_lengths2 = test_digraph2.find_path_lengths()
assert max(test_path_lengths2) == 154

real_graph = Graph(INPUT_FILE)
real_digraph = DiGraph(real_graph)
real_path_lengths = real_digraph.find_path_lengths()
print(f'Day {DAY} part 1: {max(real_path_lengths)}')
real_graph2 = Graph(INPUT_FILE, True)
real_digraph2 = DiGraph(real_graph2)
real_path_lengths2 = real_digraph2.find_path_lengths()
print(f'Day {DAY} part 2: {max(real_path_lengths2)}')
