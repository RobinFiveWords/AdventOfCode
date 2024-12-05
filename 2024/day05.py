from collections import defaultdict
import numpy as np

from aoc import parse_ints, single

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

def parse_input(file):
  with open(file) as f:
    sections = f.read().strip().split('\n\n')
  rules = defaultdict(set)
  for lower, upper in [parse_ints(line) for line in sections[0].split('\n')]:
    rules[lower].add(upper)
  updates = [parse_ints(line) for line in sections[1].split('\n')]
  return rules, updates

# I reasoned out that there's a cycle to the sort order...

def make_cycle(rules):
  length = single(list(map(len, rules.values())))
  start = list(rules)[0]
  first_half = [None] * length
  for a in rules[start]:
    first_half[length - 1 - len(rules[start] & rules[a])] = a
  restart = first_half[-1]
  second_half = [None] * length
  for a in rules[restart]:
    second_half[length - 1 - len(rules[restart] & rules[a])] = a
  last = second_half[-1]
  assert length - 1 == len(rules[last] & rules[start])
  cycle = np.array([start] + first_half + second_half)
  assert cycle.size == len(rules)
  return cycle

# ...although I may have made it more complicated than necessary.
# It may be that the problem requires all values to be within the first half
# starting from the first number in the "update", requiring only one `np.roll`.

class Cycle:
  def __init__(self, rules):
    self.rules = rules
    self.cycle = make_cycle(rules)
    self.limit = len(self.cycle) // 2

  def check(self, update):
    assert len(update) % 2 == 1  # otherwise there's no middle
    cycle = np.roll(self.cycle, -np.where(self.cycle == update[0])[0][0])
    for i in range(1, len(update)):
      distance = np.where(cycle == update[i])[0][0]
      if distance > self.limit:
        return 0
      cycle = np.roll(cycle, -distance)
    return update[len(update) // 2]

  def check2(self, update):
    correct = True
    cycle = np.roll(self.cycle, -np.where(self.cycle == update[0])[0][0])
    for i in range(1, len(update)):
      distance = np.where(cycle == update[i])[0][0]
      if distance > self.limit:
        correct = False
      cycle = np.roll(cycle, -distance)
    if correct:
      return 0
    d = {}
    for k in update:
      d[k] = [v for v in self.rules[k] if v in update]
    corrected = [x[0] for x in sorted(
        d.items(), key=lambda y: len(y[1]), reverse=True)]
    return corrected[len(corrected) // 2]

  def total(self, updates, method):
    return sum(getattr(self, method)(update) for update in updates)

def main():
  rules, updates = parse_input(INPUT_FILE)
  c = Cycle(rules)
  print(f'Day {DAY} part 1: {c.total(updates, "check")}')
  print(f'Day {DAY} part 2: {c.total(updates, "check2")}')
  pass

if __name__ == '__main__':
  main()
