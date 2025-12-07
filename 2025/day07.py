

def parse_file(file):
  with open(file) as f:
    return f.read().strip().split('\n')[::2]


def splits(lines):
  result = 0
  before = f".{lines[0].replace('S', '|')}."
  for line in lines[1:]:
    after = f".{line}."
    working = ['.'] * len(after)
    for i in range(1, len(after) - 1):
      if before[i] == '|' and after[i] == '^':
        result += 1
      if (   (after[i+1] == '^' and before[i+1] == '|')
          or (after[i-1] == '^' and before[i-1] == '|')
          or (after[i] == '.' and before[i] == '|')):
        working[i] = '|'
    before = ''.join(working)
  return result

assert splits(parse_file('testinput07.txt')) == 21


CHARS = {
  '.': 0,
  'S': 1,
  '|': 1,
  '^': -1,
}


def parse_file2(file):
  with open(file) as f:
    return [[CHARS[char] for char in line]
            for line in f.read().strip().split('\n')[::2]]


def timelines(rows):
  before = rows[0]
  for after in rows[1:]:
    working = [0] * len(after)
    for i, aval in enumerate(after):
      bval = before[i]
      if aval == -1:
        if i > 0:
          working[i-1] += bval
        if i < len(after) - 1:
          working[i+1] += bval
      else:
        working[i] += bval
    before = working[:]
  return sum(before)

assert timelines(parse_file2('testinput07.txt')) == 40


print('Day 7 part 1:', splits(parse_file('input07.txt')))
print('Day 7 part 2:', timelines(parse_file2('input07.txt')))
