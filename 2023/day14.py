import numpy as np
from aoc import flatten

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

char_map = {'O': 0, '.': 1, '#': 2}
display_map = {v: k for k, v in char_map.items()}

def parse_input(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  arr = np.full((len(lines) + 2, len(lines[0]) + 2), 2, dtype=np.int8)
  for row, line in enumerate(lines, start=1):
    for col, char in enumerate(line, start=1):
      arr[row, col] = char_map[char]
  return arr

def display(arr):
  for row in arr[1:-1]:
    print(''.join(display_map[val] for val in row[1:-1]))

def nw_col(arr1):
  where = np.where(arr1 == 2)[0]
  for i in range(len(where) - 1):
    arr1[where[i]+1:where[i+1]].sort()

def se_col(arr1):
  where = np.where(arr1 == 2)[0]
  for i in range(len(where) - 1):
    arr1[where[i]+1:where[i+1]].sort()
    arr1[where[i]+1:where[i+1]] = arr1[where[i]+1:where[i+1]][::-1]

def north(arr2): np.apply_along_axis(nw_col, 0, arr2)
def west(arr2):  np.apply_along_axis(nw_col, 1, arr2)
def south(arr2): np.apply_along_axis(se_col, 0, arr2)
def east(arr2):  np.apply_along_axis(se_col, 1, arr2)

def total_load(arr):
  result = 0
  for i in range(1, arr.shape[0] - 1):
    result += (arr.shape[0] - 1 - i) * (arr[i, 1:-1] == 0).sum()
  return result


test_arr = parse_input(TEST_INPUT_FILE)
north(test_arr)
assert total_load(test_arr) == 136

real_arr = parse_input(INPUT_FILE)
north(real_arr)
print(f'Day {DAY} part 1: {total_load(real_arr)}')


BIG_N = 1000000000
directions = [north, west, south, east]

# def compute_loads(arr, cycles):
#   loads = []
#   for _ in range(cycles):
#     for direction in directions:
#       direction(arr)
#     loads.append(total_load(arr))
#   return loads
  
# def find_cycle(loads, maximum=100):
#   i = 1
#   while i <= maximum:
#     if loads[-maximum:] == loads[-maximum - i:-i]:
#       return i
#     i += 1
#   return 0

# def find_bigN(loads, maximum=100):
#   cycle_length = find_cycle(loads, maximum)
#   assert cycle_length > 0
#   additional_cycles, remainder = divmod(BIG_N - len(loads), cycle_length)
#   return loads[-(remainder + 1)]

def get_state(arr):
  return int(''.join(str(n) for n in flatten(arr[1:-1, 1:-1]) if n != 2), 2)

def find_bigN_repeat(file):
  arr = parse_input(file)
  cycle = 0
  states = {get_state(arr): cycle}
  loads = {cycle: total_load(arr)}
  while True:
    cycle += 1
    for direction in directions:
      direction(arr)
    new_state = get_state(arr)
    if new_state in states:
      previous_cycle = states[new_state]
      cycle_length = cycle - previous_cycle
      break
    else:
      states[new_state] = cycle
      loads[cycle] = total_load(arr)
  return loads[previous_cycle + ((BIG_N - cycle) % cycle_length)]

# test_loads = compute_loads(parse_input(TEST_INPUT_FILE), 1000)
# assert find_bigN(test_loads) == 64
assert find_bigN_repeat(TEST_INPUT_FILE) == 64

# real_loads = compute_loads(parse_input(INPUT_FILE), 1000)
# print(f'Day {DAY} part 2: {find_bigN(real_loads)}')
print(f'Day {DAY} part 2: {find_bigN_repeat(INPUT_FILE)}')
