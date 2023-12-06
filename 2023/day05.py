from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

def parse_input(file):
  with open(file) as f:
    paragraphs = f.read().strip().split('\n\n')
  seeds = parse_ints(paragraphs[0])
  maps = list(map(get_map, paragraphs[1:]))
  return seeds, maps

def convert_line(s):
  destination_start, source_start, length = parse_ints(s)
  return source_start, source_start + length, destination_start - source_start

def get_map(s):
  lines = s.strip().split('\n')
  source, _, destination = lines[0].split()[0].split('-')
  return sorted(convert_line(line) for line in lines[1:])

def adjust_value(value, mp):
  for rng in mp:
    if value >= rng[0] and value < rng[1]:
      return value + rng[2]
  return value

def get_location(value, maps):
  for mp in maps:
    value = adjust_value(value, mp)
  return value

def lowest_location(seeds, maps):
  return min(get_location(value, maps) for value in seeds)

def lowest_location2(seeds, maps):
  result = float('inf')
  for i in range(0, len(seeds), 2):
    for seed in range(seeds[i], seeds[i] + seeds[i+1]):
      if (new_result := get_location(seed, maps)) < result:
        result = new_result
  return result

# but of course linear time is not good enough

def adjust_range(lo, hi, mp):
  results = []
  for rng in mp:
    if lo >= rng[1]:
      continue
    if lo < rng[0]:
      if hi <= rng[0]:
        results.append((lo, hi))
        break
      elif hi <= rng[1]:
        results.append((lo, rng[0]))
        results.append((rng[0] + rng[2], hi + rng[2]))
        break
      else:  # hi > rng[1]
        results.append((lo, rng[0]))
        results.append((rng[0] + rng[2], rng[1] + rng[2]))
        lo = rng[1]
    else:  # rng[0] <= lo < rng[1]
      if hi <= rng[1]:
        results.append((lo + rng[2], hi + rng[2]))
        break
      else:  # hi > rng[1]
        results.append((lo + rng[2], rng[1] + rng[2]))
        lo = rng[1]
  if lo >= rng[1]:  # if we continued on the last map
    results.append((lo, hi))
  return results

def get_location_range(lo, hi, maps):
  ranges = [(lo, hi)]
  next_ranges = []
  for mp in maps:
    for l, h in ranges:
      next_ranges.extend(adjust_range(l, h, mp))
    ranges = next_ranges[:]
    next_ranges = []
  return sorted(ranges)

def lowest_location_range(seeds, maps):
  ranges = []
  for i in range(0, len(seeds), 2):
    ranges.extend(get_location_range(seeds[i], seeds[i] + seeds[i+1], maps))
  return sorted(ranges)[0][0]

test_seeds, test_maps = parse_input(TEST_INPUT_FILE)
assert lowest_location(test_seeds, test_maps) == 35
assert lowest_location2(test_seeds, test_maps) == 46
assert lowest_location_range(test_seeds, test_maps) == 46

real_seeds, real_maps = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {lowest_location(real_seeds, real_maps)}')
print(f'Day {DAY} part 2: {lowest_location_range(real_seeds, real_maps)}')
