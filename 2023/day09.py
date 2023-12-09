import numpy as np

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

def parse_input(file):
  with open(file) as f:
    return [[int(n) for n in line.split()]
            for line in f.read().strip().split('\n')]

def predict_next(ints):
  arr = np.array(ints)
  result = arr[-1]
  while np.any(arr):
    arr = np.diff(arr)
    result += arr[-1]
  return result

def predict_previous(ints):
  arr = np.array(ints)
  values = [arr[0]]
  while np.any(arr):
    arr = np.diff(arr)
    values.append(arr[0])
  result = 0
  for value in values[:-1][::-1]:
    result = value - result
  return result

def predict_all(rows, func):
  return sum(map(func, rows))

test_rows = parse_input(TEST_INPUT_FILE)
assert predict_all(test_rows, predict_next) == 114
assert predict_all(test_rows, predict_previous) == 2

real_rows = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {predict_all(real_rows, predict_next)}')
print(f'Day {DAY} part 2: {predict_all(real_rows, predict_previous)}')
