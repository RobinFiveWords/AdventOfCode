

def parse_file(file):
  with open(file) as f:
    return f.read().strip().split('\n')


def maximum_joltage(bank):
  tens_digit = '0'
  ones_digit = '0'
  for i, d in enumerate(bank[:-1]):
    if d > tens_digit:
      tens_digit = d
      ones_digit = '0'
      continue
    if d > ones_digit:
      ones_digit = d
  d = bank[-1]
  if d > ones_digit:
    ones_digit = d
  return int(f"{tens_digit}{ones_digit}")


def max_pop1(s):
  return max(''.join(s[:i] + s[i+1:]) for i in range(len(s)))


def joltage_N(bank, N=12):
  current = bank[-N:]
  consider = bank[-N-1::-1]
  for candidate in consider:
    current = max_pop1(candidate + current)
  return int(current)


def total_joltage(file, func):
  return sum(func(bank) for bank in parse_file(file))

assert total_joltage('testinput03.txt', maximum_joltage) == 357
assert total_joltage('testinput03.txt', joltage_N) == 3121910778619

print('Day 3 part 1:', total_joltage('input03.txt', maximum_joltage))
print('Day 3 part 2:', total_joltage('input03.txt', joltage_N))
