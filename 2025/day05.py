from aoc import parse_ints

def parse_file(file):
  with open(file) as f:
    ranges, ingredients = f.read().strip().split('\n\n')
  return (parse_ints(ingredients),
          sorted((tuple(parse_ints(s)) for s in ranges.split('\n')),
                 key=lambda t: (t[0], -t[1])))


def fresh(ingredient, ranges):
  for lo, hi in ranges:
    if ingredient < lo:
      return False
    if ingredient <= hi:
      return True
  return False


def count_fresh(ingredients, ranges):
  return sum(fresh(ingredient, ranges) for ingredient in ingredients)

assert count_fresh(*parse_file('testinput05.txt'))


def considered_fresh(ranges):
  result = 0
  current_lo, current_hi = ranges[0]
  for next_lo, next_hi in ranges[1:]:
    if next_hi <= current_hi:
      continue
    if next_lo > current_hi + 1:
      result += current_hi - current_lo + 1
      current_lo, current_hi = next_lo, next_hi
      continue
    current_hi = next_hi
  result += current_hi - current_lo + 1
  return result

assert considered_fresh(parse_file('testinput05.txt')[1]) == 14


print('Day 5 part 1:', count_fresh(*parse_file('input05.txt')))
print('Day 5 part 2:', considered_fresh(parse_file('input05.txt')[1]))
