import numpy as np

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

XMAS = 'XMAS'
TARGETS1 = [XMAS, XMAS[::-1]]
MAS = 'MAS'
TARGETS2 = [MAS, MAS[::-1]]

def parse_input(file):
  with open(file) as f:
    return np.array([list(line) for line in f.read().strip().split('\n')])

def count1(arr):
  result = 0
  rows, cols = arr.shape
  # E-W
  for row in range(rows):
    for col in range(cols - 3):
      if ''.join(arr[row, col:col+4].squeeze()) in TARGETS1:
        result += 1
  # N-S
  for row in range(rows - 3):
    for col in range(cols):
      if ''.join(arr[row:row+4, col].squeeze()) in TARGETS1:
        result += 1
  # NW-SE and SW-NE
  for row in range(rows - 3):
    for col in range(cols - 3):
      if ''.join([arr[row+d, col+d] for d in range(4)]) in TARGETS1:
        result += 1
      if ''.join([arr[row+d, col+3-d] for d in range(4)]) in TARGETS1:
        result += 1
  return result

def count2(arr):
  result = 0
  rows, cols = arr.shape
  for row in range(rows - 2):
    for col in range(cols - 2):
      if (''.join([arr[row+d, col+d] for d in range(3)]) in TARGETS2 and
          ''.join([arr[row+d, col+2-d] for d in range(3)]) in TARGETS2):
        result += 1
  return result

def main():
  print(f'Day {DAY} part 1: {count1(parse_input(INPUT_FILE))}')
  print(f'Day {DAY} part 2: {count2(parse_input(INPUT_FILE))}')
  pass

if __name__ == '__main__':
  main()
