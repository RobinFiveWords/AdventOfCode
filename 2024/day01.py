import sys
from collections import Counter

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'
TEST_INPUT_FILE = f'test{INPUT_FILE}'

def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  A = []
  B = []
  [(A.append(a), B.append(b)) for a, b in map(parse_ints, lines)]
  return sorted(A), sorted(B)

def total_distance(A, B):
  return sum(abs(a - b) for a, b in zip(A, B))

def parse_file2(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  A = Counter()
  B = Counter()
  for a, b in map(parse_ints, lines):
    A[a] += 1
    B[b] += 1
  return A, B

def similarity_score(A, B):
  return sum(k * v * B[k] for k, v in A.items())

def test():
  assert 11 == total_distance(*parse_file(TEST_INPUT_FILE))
  assert 31 == similarity_score(*parse_file2(TEST_INPUT_FILE))
  print('Tests pass.')

def main():
  print(f'Day {DAY} part 1: {total_distance(*parse_file(INPUT_FILE))}')
  print(f'Day {DAY} part 2: {similarity_score(*parse_file2(INPUT_FILE))}')

if __name__ == '__main__':
  if len(sys.argv) > 1:
    test()
  else:
    main()
