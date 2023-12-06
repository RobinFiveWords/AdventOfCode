import math

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

def parse_input(file):
  with open(file) as f:
    times, distances = list(map(parse_ints, f.read().strip().split('\n')))
  return list(zip(times, distances))

def get_distance(total_time, hold_time):
  return hold_time * (total_time - hold_time)

def ways_to_beat_record(total_time, current_record):
  ways = 0
  for hold_time in range(1, total_time):
    distance = get_distance(total_time, hold_time)
    if distance > current_record:
      ways += 1
  return ways

def total_ways(races):
  return math.prod(ways_to_beat_record(time, distance)
                   for time, distance in races)

def concatenate_input(races):
  times, distances = zip(*races)
  time = int(''.join(str(n) for n in times))
  distance = int(''.join(str(n) for n in distances))
  return time, distance

class BinarySearch:
  def __init__(self, total_time, current_record):
    assert (total_time // 2) ** 2 > current_record
    self.total_time = total_time
    self.current_record = current_record
    self.distances = {}

  def run(self):
    self.search_lo()
    self.search_hi()
    times, distances = list(zip(*sorted(self.distances.items())))
    beats_record = [distance > self.current_record for distance in distances]
    start = beats_record.index(True)
    end = start + beats_record[start:].index(False) - 1
    return times[end] - times[start] + 1

  def get(self, time):
    if time in self.distances:
      return self.distances[time]
    else:
      distance = get_distance(self.total_time, time)
      self.distances[time] = distance
      return distance

  def search_lo(self):
    lo = 1
    hi = self.total_time // 2
    while True:
      distance_lo = self.get(lo)
      distance_hi = self.get(hi)
      mid = lo + (hi - lo) // 2
      distance_mid = self.get(mid)
      if hi - lo <= 1:
        break
      if distance_mid > self.current_record:  # search below
        hi = mid
      else:
        lo = mid

  def search_hi(self):
    lo = self.total_time // 2
    hi = self.total_time - 1
    while hi - lo > 1:
      distance_lo = self.get(lo)
      distance_hi = self.get(hi)
      mid = lo + (hi - lo) // 2
      distance_mid = self.get(mid)
      if hi - lo <= 1:
        break
      if distance_mid > self.current_record:  # search above
        lo = mid
      else:
        hi = mid

test_races = parse_input(TEST_INPUT_FILE)
assert total_ways(test_races) == 288
test_race2 = concatenate_input(test_races)
test_search = BinarySearch(*test_race2)
assert test_search.run() == 71503

real_races = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {total_ways(real_races)}')
real_race2 = concatenate_input(real_races)
real_search = BinarySearch(*real_race2)
print(f'Day {DAY} part 2: {real_search.run()}')
