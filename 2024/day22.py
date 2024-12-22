from collections import defaultdict
import numpy as np

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

def evolve(secret):
  secret = ((secret * 64) ^ secret) % 16777216
  secret = ((secret // 32) ^ secret) % 16777216
  return ((secret * 2048) ^ secret) % 16777216 

def evolve_file(file, n):
  with open(file) as f:
    secrets = parse_ints(f.read())
  for _ in range(n):
    secrets = list(map(evolve, secrets))
  return secrets


class Market:
  def __init__(self, file):
    with open(file) as f:
      self.initial_secrets = parse_ints(f.read())
    secrets = self.initial_secrets
    prices = []
    prices.append([n % 10 for n in secrets])
    for _ in range(2000):
      secrets = list(map(evolve, secrets))
      prices.append([n % 10 for n in secrets])
    self.p = np.array(prices)  # each row is a generation, each column a monkey
    self.c = np.diff(self.p, axis=0)
    self.bests = defaultdict(int)
    self.seen = [set() for _ in range(self.c.shape[1])]
    for i, monkey in enumerate(self.c.T):
      for j in range(4, monkey.size):
        t = tuple(monkey[j-4:j])
        if t in self.seen[i]:
          continue
        self.seen[i].add(t)
        self.bests[t] += self.p[j, i]



def main():
  print(f'Day {DAY} part 1: {sum(evolve_file(INPUT_FILE, 2000))}')
  print(f'Day {DAY} part 2: {max(Market(INPUT_FILE).bests.values())}')
  pass

if __name__ == '__main__':
  main()
