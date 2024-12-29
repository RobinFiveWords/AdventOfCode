from collections import Counter
from functools import cache

from aoc import flatten, parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

def parse_file(file):
  with open(file) as f:
    return f.read().strip()

@cache
def evolve(stone):
  if stone == 0:
    return (1,)
  half_length = len(str(stone)) / 2
  if half_length == int(half_length):
    return tuple(map(int, divmod(stone, 10 ** half_length)))
  else:
    return (2024 * stone,)

def append(stones, repeat=1):
  for blinks in range(1, repeat + 1):
    stones.append(list(flatten(evolve(stone) for stone in stones[-1])))

def evolve_collection(c, repeat=1):
  current = c.copy()
  pending = Counter()
  for _ in range(repeat):
    for n, quantity in current.items():
      result = evolve(n)
      for new in result:
        pending[new] += quantity
    current = pending.copy()
    pending = Counter()
  return current

def main():
  real_stones = [parse_ints(parse_file(INPUT_FILE))]
  append(real_stones, 25)
  print(f'Day {DAY} part 1: {len(real_stones[-1])}')
  real_stones2 = Counter(parse_ints(parse_file(INPUT_FILE)))
  print(f'Day {DAY} part 2: {sum(evolve_collection(real_stones2, 75).values())}')
  pass

if __name__ == '__main__':
  main()
