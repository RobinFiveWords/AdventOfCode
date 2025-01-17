from collections import Counter, defaultdict
from pprint import pprint

from aoc import parse_ints, Point, Origin, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

DIRECTIONS = {
  Up: '^',
  Down: 'v',
  Left: '<',
  Right: '>',
}

numeric_keypad = {
  'A': Origin,
  '0': Point(-1,  0),
  '1': Point(-2, -1),
  '2': Point(-1, -1),
  '3': Point( 0, -1),
  '4': Point(-2, -2),
  '5': Point(-1, -2),
  '6': Point( 0, -2),
  '7': Point(-2, -3),
  '8': Point(-1, -3),
  '9': Point( 0, -3),
}

directional_keypad = {
  'A': Origin,
  '^': Point(-1,  0),
  '<': Point(-2,  1),
  'v': Point(-1,  1),
  '>': Point( 0,  1),
}

def shortest_paths(keypad):
  shortest = defaultdict(list)
  labels = {v: k for k, v in keypad.items()}
  for label_from, point_from in keypad.items():
    shortest[(label_from, label_from)].append(())
    current = [(point_from, ())]
    visited = set(point for point, path in current)
    pending = set()
    while current:
      complete = visited.copy()
      this_round = set()
      for point, path in current:
        for direction in DIRECTIONS:
          neighbor = point + direction
          if neighbor in complete:
            continue
          if neighbor not in keypad.values():
            continue
          label_to = labels[neighbor]
          new_path = path + (direction, )
          shortest[(label_from, label_to)].append(new_path)
          pending.add((neighbor, new_path))
          this_round.add(neighbor)
      visited.update(this_round)
      current = list(pending)
      pending = set()
  return shortest

def product(*iterables):
  # recipe starting from
  # https://docs.python.org/3/library/itertools.html#itertools.product
  # because itertools.product bails at an empty list
  pools = [tuple(pool) for pool in iterables]
  result = [[]]
  for pool in pools:
    if pool:
      result = [x+[y] for x in result for y in pool]
    else:
      result = [x+[()] for x in result]
  return result

def get_combos(shortest, code=None):
  if code:
    code = 'A' + code
    shortest = {k: v for k, v in shortest.items()
                for i in range(len(code) - 1)
                if k == (code[i], code[i+1])}
  return product(*shortest.values()), list(shortest.keys())

def get_sequences(combo):
  return [f"A{''.join([DIRECTIONS[direction] for direction in L])}A"
          for L in combo]

def get_next_level(from_to, sequence):
  return {ft: Counter((s[i], s[i+1]) for i in range(len(s) - 1))
          for ft, s in zip(from_to, sequence)}

def get_next_levels(shortest, code=None):
  combos, from_to = get_combos(shortest, code)
  return [get_next_level(from_to, get_sequences(combo))
          for combo in combos]

def expand(code, numeric_next_level, directional_next_level, directional_robots):
  s = 'A' + code
  start = Counter((s[i], s[i+1]) for i in range(len(s) - 1))
  counts = [start]
  c = Counter()
  for step, frequency in counts[-1].items():
    for next_step, next_frequency in numeric_next_level[step].items():
      c[next_step] += frequency * next_frequency
  counts.append(c)
  for _ in range(directional_robots):
    c = Counter()
    for step, frequency in counts[-1].items():
      for next_step, next_frequency in directional_next_level[step].items():
        c[next_step] += frequency * next_frequency
    counts.append(c)
  return counts

def get_min_length(counts):
  return min(sum(count.values()) for count in counts)

def find_min_length(code, directional_robots):
  spn = shortest_paths(numeric_keypad)
  nln = get_next_levels(spn, code)
  spd = shortest_paths(directional_keypad)
  nld = get_next_levels(spd)
  results = [expand(code, n, d, directional_robots)
             for n in nln
             for d in nld]
  return get_min_length(counts[-1] for counts in results)

def complexity(code, directional_robots):
  ints = parse_ints(code)
  assert len(ints) == 1
  return ints[0] * find_min_length(code, directional_robots)

def complexities(codes, directional_robots):
  return sum(map(lambda code: complexity(code, directional_robots), codes))

def parse_input(file):
  with open(file) as f:
    return f.read().strip().split('\n')

assert complexities(parse_input(TEST_INPUT_FILE), 2) == 126384

print(f"Day {DAY} part 1: {complexities(parse_input(INPUT_FILE), 2)}")
print(f"Day {DAY} part 2: {complexities(parse_input(INPUT_FILE), 25)}")
