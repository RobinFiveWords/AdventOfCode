import functools
import itertools

from aoc import flatten

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

ZERO = (0, )

BRUTE_FORCE_SYMBOLS = 20

def parse_file(file):
  with open(file) as f:
    return f.read().strip().split('\n')

def join_ints(L):
  return ','.join(str(n) for n in L)

def extend(s, n):
  s1, s2 = s.split()
  return f"{'?'.join([s1] * n)} {','.join([s2] * n)}"

@functools.cache
def get_compositions(n, k):
  compositions = set()
  if n < k or k == 0:
    return compositions
  if n == k:
    compositions.add(tuple([1] * n))
    return compositions
  if k == 1:
    compositions.add((n, ))
    return compositions
  # add a part
  for comp in get_compositions(n - 1, k - 1):
    for i in range(k + 1):
      compositions.add(tuple(comp[:i] + (1, ) + comp[i:]))
  # add to an existing part
  for comp in get_compositions(n - 1, k):
    for i in range(k):
      compositions.add(tuple(comp[:i] + (comp[i] + 1, ) + comp[i+1:]))
  return compositions

@functools.cache
def get_spacers(total, runs):
  # print(f"get_spacers({total}, {runs})")
  if total == 0:
    compositions = set()
    if runs > 1:
      return compositions
    compositions.add((0, 0))
    return compositions
  compositions_neither = get_compositions(total, runs + 1)
  compositions_left    = set(tuple(ZERO + comp)
                             for comp in get_compositions(total, runs))
  compositions_right   = set(tuple(comp[1:] + ZERO)
                             for comp in compositions_left)
  compositions_both    = set(tuple(ZERO + comp + ZERO)
                             for comp in get_compositions(total, runs - 1))
  return (compositions_neither
        | compositions_left
        | compositions_right
        | compositions_both)

@functools.cache
def compute(s):
  try:
    symbols, numbers = s.split()
  except ValueError:  # no runs i.e. no damaged
    if '#' in s:
      return 0  # at least one damaged -> contradiction
    else:
      return 1  # all operational
  runs = [int(n) for n in numbers.split(',')]
  known = {i: symbol for i, symbol in enumerate(symbols) if symbol  != '?'}
  if sum(v == '#' for v in known.values()) > sum(runs):
    return 0  # too many damaged -> contradiction
  if sum(runs) + len(runs) - 1 > len(symbols):
    return 0  # not enough symbols -> contradiction

  if len(symbols) <= BRUTE_FORCE_SYMBOLS:  # brute force
    result = 0
    spacers = get_spacers(len(symbols) - sum(runs), len(runs))
    for spacer in spacers:
      candidate = ''.join(list(flatten(
          itertools.zip_longest(('.' * s for s in spacer),
                                ('#' * r for r in runs))))[:-1])
      if all(char == candidate[i] for i, char in known.items()):
        result += 1
    return result

  # If the longest run is n,
  # any given subset of n+1 has at least one operational.
  # We're going to pick a split point and test each of those n+1.
  longest_run = max(runs)
  result = 0
  s_brute_force = symbols[:BRUTE_FORCE_SYMBOLS]
  if '.' in s_brute_force:
    start = len(s_brute_force) - s_brute_force[::-1].index('.') - 1
    end = start + 1
  else:
    start = BRUTE_FORCE_SYMBOLS - longest_run - 1
    end = BRUTE_FORCE_SYMBOLS
  s_start = symbols[:start]
  for i in range(start, end):
    # index i is first index >= start that is operational
    if symbols[i] == '#':
      continue
    # consider all starting subsets of runs that will fit
    r = 0
    cumulative = 0
    while r < len(runs):
      new_cumulative = cumulative + (1 if r > 0 else 0) + runs[r]
      if new_cumulative > i:
        break
      cumulative = new_cumulative
      r += 1
    # all >= start and < i must be damaged
    s_i = s_start + ('#' * (i - start))
    for j in range(0, r + 1):
      first = compute(f"{s_i} {join_ints(runs[:j])}")
      if first > 0:
        result += first * \
            compute(f"{symbols[i+1:]} {join_ints(runs[j:])}")
  return result

def run_tests():
  ts = parse_file(TEST_INPUT_FILE)
  assert [compute(t) for t in ts] == [1, 4, 1, 1, 4, 10]
  assert [compute(extend(t, 5)) for t in ts] == [1, 16384, 1, 16, 2500, 506250]

run_tests()
lines = parse_file(INPUT_FILE)
results1 = [compute(line) for line in lines]
print(f'Day {DAY} part 1: {sum(results1)}')
results5 = [compute(extend(line, 5)) for line in lines]
print(f'Day {DAY} part 2: {sum(results5)}')
