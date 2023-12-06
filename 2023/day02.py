import collections
import math
import re

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

TARGET = {'red': 12, 'green': 13, 'blue': 14}

def count_game(s):
  label, outcomes = s.split(':')
  game_id = int(re.search(r'\d+', label).group(0))
  colors = list(re.findall(r'[a-z]+', outcomes))
  quantities = [int(n) for n in re.findall(r'\d+', outcomes)]
  most_seen = collections.defaultdict(int)
  for color, quantity in zip(colors, quantities):
    if quantity > most_seen[color]:
      most_seen[color] = quantity
  return game_id, most_seen

def possible(d, target=TARGET):
  for color in d:
    if d[color] > TARGET[color]:
      return False
  return True

def sum_of_possible(file):
  with open(file) as f:
    games = f.read().strip().split('\n')
  return sum(game_id for game_id, most_seen in map(count_game, games)
             if possible(most_seen))

def power(d):
  try:
    return d['red'] * d['green'] * d['blue']
  except KeyError:
    return 0

def sum_of_power(file):
  with open(file) as f:
    games = f.read().strip().split('\n')
  return sum(power(most_seen) for game_id, most_seen in map(count_game, games))

assert sum_of_possible(TEST_INPUT_FILE) == 8
assert sum_of_power(TEST_INPUT_FILE) == 2286

print(f'Day {DAY} part 1: {sum_of_possible(INPUT_FILE)}')
print(f'Day {DAY} part 2: {sum_of_power(INPUT_FILE)}')
