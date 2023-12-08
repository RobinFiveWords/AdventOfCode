import itertools
import math
import re

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')
TEST_INPUT_FILE2 = INPUT_FILE.replace('input', 'testinput2')
TEST_INPUT_FILE3 = INPUT_FILE.replace('input', 'testinput3')

DIRECTIONS = {'L': 0, 'R': 1}

def parse_input(file):
  with open(file) as f:
    ds, ns = f.read().strip().split('\n\n')
  directions = [DIRECTIONS[char] for char in ds]
  nodes = {}
  for row in ns.split('\n'):
    node, left, right = re.findall(r'\w+', row)
    nodes[node] = (left, right)
  return directions, nodes

def follow_instructions(directions, nodes, start='AAA', end='ZZZ'):
  current = start
  steps = 0
  moves = itertools.cycle(directions)
  while current != end:
    move = next(moves)
    current = nodes[current][move]
    steps += 1
  return steps

def ghost(directions, nodes, start, end_char, maximum=100_000):
  zs = []
  current = start
  steps = 0
  moves = itertools.cycle(directions)
  while steps < maximum:
    move = next(moves)
    current = nodes[current][move]
    steps += 1
    if current[-1] == end_char:
      zs.append(steps)
  return zs

def ghost_instructions(directions, nodes, start_char='A', end_char='Z', maximum=100_000):
  ghosts = [ghost(directions, nodes, start, end_char, maximum)
            for start in nodes if start[-1] == start_char]
  assert all(zs[0] * 2 == zs[1] for zs in ghosts)  # these are repeating cycles
  return math.lcm(*(zs[0] for zs in ghosts))

test_directions, test_nodes = parse_input(TEST_INPUT_FILE)
assert follow_instructions(test_directions, test_nodes) == 2
test_directions2, test_nodes2 = parse_input(TEST_INPUT_FILE2)
assert follow_instructions(test_directions2, test_nodes2) == 6

test_directions3, test_nodes3 = parse_input(TEST_INPUT_FILE3)
assert ghost_instructions(test_directions3, test_nodes3) == 6

real_directions, real_nodes = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {follow_instructions(real_directions, real_nodes)}')
print(f'Day {DAY} part 2: {ghost_instructions(real_directions, real_nodes)}')
