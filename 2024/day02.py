import sys
from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'
TEST_INPUT_FILE = f'test{INPUT_FILE}'

def parse_input(file):
  with open(file) as f:
    return [parse_ints(line) for line in f.read().strip().split('\n')]

def safe(report):
  report_sorted = sorted(report)
  if report != report_sorted and report != report_sorted[::-1]:
    return False
  for i in range(len(report) - 1):
    if not 1 <= abs(report[i] - report[i+1]) <= 3:
      return False
  return True

def try_safe(report):
  return safe(report) or any(safe(report[:n] + report[n+1:]) for n in range(len(report)))

def test():
  assert sum(map(safe, parse_input(TEST_INPUT_FILE))) == 2
  assert sum(map(try_safe, parse_input(TEST_INPUT_FILE))) == 4
  print('Tests pass.')

def main():
  print(f'Day {DAY} part 1: {sum(map(safe, parse_input(INPUT_FILE)))}')
  print(f'Day {DAY} part 2: {sum(map(try_safe, parse_input(INPUT_FILE)))}')

if __name__ == '__main__':
  if len(sys.argv) > 1:
    test()
  else:
    main()
