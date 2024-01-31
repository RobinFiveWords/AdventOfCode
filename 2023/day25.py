import collections
import copy
import itertools
import sys

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')


class Graph:
  def __init__(self, file):
    self.adj = collections.defaultdict(list)
    with open(file) as f:
      lines = f.read().strip().split('\n')
    for line in lines:
      tokens = line.replace(':', '').split()
      v0 = tokens[0]
      for v in tokens[1:]:
        self.adj[v0].append(v)
        self.adj[v].append(v0)
    self.shortest_paths = collections.defaultdict(dict)
    for v in sorted(self.adj.keys()):
      self.find_shortest_paths(v)

  def find_shortest_paths(self, starting_v):
    visited = set()
    visited.add(starting_v)
    current = [starting_v]
    pending = set()
    distance = 0
    while current:
      distance += 1
      for v in current:
        neighbors = self.adj[v]
        for n in neighbors:
          if n in visited:
            continue
          visited.add(n)
          if n not in self.shortest_paths[starting_v]:
            self.shortest_paths[starting_v][n] = distance
            self.shortest_paths[n][starting_v] = distance
          pending.add(n)
      current = list(pending)
      pending = set()

  def find_candidate_edges(self, n=100):
    closest = sorted((sum(self.shortest_paths[v].values()), v) for v in self.adj)
    vs = [t[1] for t in closest[:n]]
    es = [(v1, v2) for v1 in vs for v2 in self.adj[v1] if v2 in vs and v1 < v2]
    return es


class ConnectedComponents:
  def __init__(self, adj, edges_to_remove):
    self.adj = copy.deepcopy(adj)
    for v1, v2 in edges_to_remove:
      self.adj[v1].remove(v2)
      self.adj[v2].remove(v1)
    self.components = {v: None for v in self.adj}
    self.get_connected_components()

  def get_connected_components(self):
    component = 0
    while None in self.components.values():
      remaining = [v for v, component in self.components.items()
                   if component is None]
      v = remaining[0]
      self.dfs_component(v, component)
      component += 1

  def dfs_component(self, v, component):
    self.components[v] = component
    for next_v in self.adj[v]:
      if self.components[next_v] is None:
        self.dfs_component(next_v, component)


def search(graph):
  for combo in itertools.combinations(graph.find_candidate_edges(), 3):
    cc = ConnectedComponents(graph.adj, combo)
    if max(cc.components.values()) == 1:
      counts = list(collections.Counter(cc.components.values()).values())
      return counts[0] * counts[1]

tg = Graph(TEST_INPUT_FILE)
assert search(tg) == 54

sys.setrecursionlimit(2000)

rg = Graph(INPUT_FILE)
print(f'Day {DAY} part 1: {search(rg)}')
