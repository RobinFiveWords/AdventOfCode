import itertools
import operator

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

OPERATORS = [operator.add, operator.mul]

def parse_input(file):
  with open(file) as f:
    return [parse_ints(line) for line in f.read().strip().split('\n')]

def possible(ints, ops):
  target, start, remaining = ints[0], ints[1], ints[2:]
  possible_operators = list(itertools.product(ops, repeat=len(remaining)))
  for operators in possible_operators:
    result = start
    for i, op in enumerate(operators):
      result = op(result, remaining[i])
    if result == target:
      return target
  return 0

def concatenate(a, b):
  return int(str(a) + str(b))

OPERATORS2 = OPERATORS + [concatenate]

# Part 2 took about 24 seconds. Could bail earlier...

def main():
  print(f'Day {DAY} part 1: {sum(map(lambda ints: possible(ints, OPERATORS), parse_input(INPUT_FILE)))}')
  print(f'Day {DAY} part 2: {sum(map(lambda ints: possible(ints, OPERATORS2), parse_input(INPUT_FILE)))}')
  pass

if __name__ == '__main__':
  main()
