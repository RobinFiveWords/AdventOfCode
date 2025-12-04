

def parse_file(file):
  with open(file) as f:
    return sorted(tuple(map(int, rng.split('-')))
                  for rng in f.read().strip().split(','))


def invalid_ids(ranges):
  result = []
  current = 1
  for r in ranges:
    while (candidate := int(str(current) * 2)) <= r[1]:
      if candidate >= r[0]:
        result.append(candidate)
      current += 1
  return result

assert sum(invalid_ids(parse_file('testinput02.txt'))) == 1227775554


def invalid_ids2(ranges):
  current = 1
  invalids = set()
  maximum = ranges[-1][1]
  while int(str(current) * 2) <= maximum:
    repeats = 2
    while (candidate := int(str(current) * repeats)) <= maximum:
      invalids.add(candidate)
      repeats += 1
    current += 1
  result = []
  invalids = sorted(invalids)
  invalid_index = 0
  range_index = 0
  while invalid_index < len(invalids) and range_index < len(ranges):
    i = invalids[invalid_index]
    r = ranges[range_index]
    if i < r[0]:
      invalid_index += 1
    elif i > r[1]:
      range_index += 1
    else:
      result.append(i)
      invalid_index += 1
  return result

assert sum(invalid_ids2(parse_file('testinput02.txt'))) == 4174379265


print('Day 2 part 1:', sum(invalid_ids(parse_file('input02.txt'))))
print('Day 2 part 2:', sum(invalid_ids2(parse_file('input02.txt'))))
