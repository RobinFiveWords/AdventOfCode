

def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  results = []
  for line in lines:
    if line[0] == 'L':
      results.append(-int(line[1:]))
    else:
      results.append(int(line[1:]))
  return results


def land_zeros(file, start=50, size=100):
  result = 0
  current = start
  for value in parse_file(file):
    current += value
    current %= size
    if current == 0:
      result += 1
  return result

assert land_zeros('testinput01.txt') == 3


def point_zeros(file, start=50, size=100):
  result = 0
  previous_position = start
  current_position = None
  diff_spins = None
  for value in parse_file(file):
    diff_spins, current_position = divmod(previous_position + value, size)
    result += abs(diff_spins) - int(previous_position == 0 and value <= 0)
    if diff_spins <= 0 and current_position == 0:
      result += 1
    previous_position = current_position
  return result

assert point_zeros('testinput01.txt') == 6


print('Day 1 part 1:', land_zeros('input01.txt'))
print('Day 1 part 2:', point_zeros('input01.txt'))
