from collections import defaultdict

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'


class Network:
  def __init__(self, file):
    with open(file) as f:
      lines = [line.split('-') for line in f.read().strip().split('\n')]
    self.adj = defaultdict(list)
    for a, b in lines:
      self.adj[a].append(b)
      self.adj[b].append(a)
    self.threes = set(frozenset((a, b, c))
                      for a in self.adj
                      for b in self.adj[a]
                      for c in self.adj[b]
                      if c in self.adj[a])
    # confirming the entire graph is a single connected component
    self.cc = {}
    self.get_connected_components()

  def t3s(self):
    return sum(1 for s in self.threes if any(e.startswith('t') for e in s))

  def get_connected_components(self):
    remaining = list(self.adj.keys())
    component = 0
    while remaining:
      current = [remaining.pop()]
      pending = set()
      while current:
        for node in current:
          self.cc[node] = component
          for neighbor in self.adj[node]:
            if neighbor not in self.cc:
              pending.add(neighbor)
              if neighbor in remaining:
                remaining.remove(neighbor)
        current = list(pending)
        pending = set()
      component += 1

  def largest_party(self, node):
    working = [[node]]
    neighbors = self.adj[node]
    for neighbor in neighbors:
      neighbor_adj = self.adj[neighbor]
      for L in working:
        if all(k in neighbor_adj for k in L):
          working.append(L + [neighbor])
    return ','.join(sorted(max(working, key=lambda L: len(L))))

  def password(self):
    return max((self.largest_party(node) for node in self.adj),
               key=lambda s: len(s))


def main():
  network = Network(INPUT_FILE)
  print(f'Day {DAY} part 1: {network.t3s()}')
  print(f'Day {DAY} part 2: {network.password()}')
  pass

if __name__ == '__main__':
  main()
