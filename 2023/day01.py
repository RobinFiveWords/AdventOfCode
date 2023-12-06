import re

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')
TEST_INPUT_FILE2 = INPUT_FILE.replace('input', 'testinput2')

regex_overlaps = re.compile(r'(?=([0-9]|one|two|three|four|five|six|seven|eight|nine))')
regex = re.compile(r'([0-9]|one|two|three|four|five|six|seven|eight|nine)')

substitutions = {
  'one': '1',
  'two': '2',
  'three': '3',
  'four': '4',
  'five': '5',
  'six': '6',
  'seven': '7',
  'eight': '8',
  'nine': '9',
}

def parse_line(line):
  digits = re.findall(r'\d', line)
  return int(digits[0] + digits[-1])

def parse_line2(line):
  indices = list(regex_overlaps.finditer(line))
  first = regex.match(line[indices[0].span()[0]:]).group(0)
  last = regex.match(line[indices[-1].span()[0]:]).group(0)
  return int(substitutions.get(first, first) + substitutions.get(last, last))

def parse_file(file, func):
  with open(file) as f:
    return [func(line) for line in f.read().strip().split('\n')]

assert sum(parse_file(TEST_INPUT_FILE, parse_line)) == 142
assert sum(parse_file(TEST_INPUT_FILE2, parse_line2)) == 281

print(f'Day {DAY} part 1: {sum(parse_file(INPUT_FILE, parse_line))}')
print(f'Day {DAY} part 2: {sum(parse_file(INPUT_FILE, parse_line2))}')
