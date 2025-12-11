import numpy as np
from scipy.optimize import milp, LinearConstraint

from aoc import parse_ints


def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  out = []
  for line in lines:
    tokens = line.split()
    length = len(tokens[0]) - 2
    target = sum(2 ** i for i, char in enumerate(tokens[0][1:-1])
                 if char == '#')
    buttons = []
    for token in tokens[1:-1]:
      buttons.append(sum(2 ** i for i in parse_ints(token)))
    out.append((length, target, buttons))
  return out


def bfs(line):
  length, target, buttons = line
  start = 0
  assert start != target
  button_presses = 0
  current = [start]
  visited = set(current)
  pending = set()
  while current:
    button_presses += 1
    for state in current:
      for button in buttons:
        next_state = state ^ button
        if next_state == target:
          return button_presses
        if next_state in visited:
          continue
        visited.add(next_state)
        pending.add(next_state)
    current = list(pending)
    pending.clear()


def parse_file2(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  out = []
  for line in lines:
    tokens = line.split()
    buttons = [parse_ints(token) for token in tokens[1:-1]]
    joltages = parse_ints(tokens[-1])
    A = np.zeros((len(joltages), len(buttons)))
    for i, button in enumerate(buttons):
      for j in button:
        A[j, i] = 1
    b = np.array(joltages)
    out.append((A, b))
  return out


def solve(line):
  A, b = line
  c = np.ones(A.shape[1])
  constraints = LinearConstraint(A, lb=b, ub=b)
  result = milp(c=c, constraints=constraints, integrality=np.ones_like(c))
  out = int(result.fun)
  assert out == result.fun
  return out


test_lines = parse_file('testinput10.txt')
assert [bfs(line) for line in test_lines] == [2, 3, 2]

test_lines2 = parse_file2('testinput10.txt')
assert [solve(line) for line in test_lines2] == [10, 12, 11]


real_lines = parse_file('input10.txt')
real_lines2 = parse_file2('input10.txt')

print('Day 10 part 1:', sum(bfs(line) for line in real_lines))
print('Day 10 part 2:', sum(solve(line) for line in real_lines2))
