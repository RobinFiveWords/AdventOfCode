import collections
import re
from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

NOT_SYMBOLS = '0123456789.\n'

NEIGHBORS = [Up, Up + Left, Left, Down + Left, Down, Down + Right, Right, Up + Right] 

def get_numbers(lines):
  numbers = collections.defaultdict(list)
  for y, line in enumerate(lines):
    current = []
    for match in re.finditer(r'\d+', line):
      number = [int(match.group(0)), set()]
      for x in range(*match.span()):
        number[1].add(Point(x, y))
      current.append(number[:])
    numbers[y] = current[:]
  return numbers

def get_symbols(lines):
  symbols = collections.defaultdict(set)
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char not in NOT_SYMBOLS:
        symbols[y].add(Point(x, y))
  return symbols

def is_part_number(y, number, symbols):
  targets = symbols[y-1] | symbols[y] | symbols[y+1]
  return any(point + neighbor in targets
             for point in number[1]
             for neighbor in NEIGHBORS)

def sum_of_part_numbers(numbers, symbols):
  result = 0
  for y, row in numbers.items():
    for number in row:
      if is_part_number(y, number, symbols):
        result += number[0]
  return result

def get_adjacent_numbers(y, symbol, numbers):
  adjacent_numbers = []
  for i in range(y - 1, y + 2):
    for number in numbers[i]:
      if any(symbol + neighbor in number[1]
             for neighbor in NEIGHBORS):
        adjacent_numbers.append(number[0])
  return adjacent_numbers

def sum_of_gear_ratios(numbers, symbols):
  result = 0
  for y, row in symbols.items():
    for symbol in row:
      adjacent_numbers = get_adjacent_numbers(y, symbol, numbers)
      if len(adjacent_numbers) == 2:
        result += adjacent_numbers[0] * adjacent_numbers[1]
  return result

with open(TEST_INPUT_FILE) as f:
  test_lines = f.read().strip().split('\n')
test_numbers = get_numbers(test_lines)
test_symbols = get_symbols(test_lines)
assert sum_of_part_numbers(test_numbers, test_symbols) == 4361
assert sum_of_gear_ratios(test_numbers, test_symbols) == 467835

with open(INPUT_FILE) as f:
  real_lines = f.read().strip().split('\n')
real_numbers = get_numbers(real_lines)
real_symbols = get_symbols(real_lines)
print(f'Day {DAY} part 1: {sum_of_part_numbers(real_numbers, real_symbols)}')
print(f'Day {DAY} part 2: {sum_of_gear_ratios(real_numbers, real_symbols)}')
