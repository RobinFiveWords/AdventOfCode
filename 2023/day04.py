import collections
import re

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

regex = re.compile(r'\d+')

def parse_file(file):
  with open(file) as f:
    return f.read().strip().split('\n')

def parse_card(card):
  first, rest = card.split(':')
  number = int(regex.search(first).group(0))
  second, third = rest.split('|')
  winning = [int(n) for n in regex.findall(second)]
  assert len(set(winning)) == len(winning)
  winning = set(winning)
  yours = [int(n) for n in regex.findall(third)]
  matches = sum(number in winning for number in yours)
  return number, matches

def sum_points(cards):
  points = 0
  for number, matches in map(parse_card, cards):
    if matches == 0:
      continue
    points += 2 ** (matches - 1)
  return points

def total_scratchcards(cards):
  d = collections.defaultdict(int)
  for card in cards:
    number, matches = parse_card(card)
    d[number] += 1
    for i in range(1, matches + 1):
      d[number + i] += d[number]
  return sum(v for k, v in d.items() if k <= len(cards))

test_cards = parse_file(TEST_INPUT_FILE)
assert sum_points(test_cards) == 13
assert total_scratchcards(test_cards) == 30

real_cards = parse_file(INPUT_FILE)
print(f'Day {DAY} part 1: {sum_points(real_cards)}')
print(f'Day {DAY} part 2: {total_scratchcards(real_cards)}')
