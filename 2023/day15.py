import re

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

def HASH(s):
  value = 0
  for char in s:
    value += ord(char)
    value += (value << 4)
    value %= 256
  return value

def parse_input(file):
  with open(file) as f:
    return f.read().strip().split(',')

delims = re.compile(r'[\-=]')

def parse_step(step):
  args = delims.split(step)
  if args[1] != '':
    return (args[0], int(args[1]))
  else:
    return (args[0], None)

class Boxes:
  def __init__(self, file):
    self.steps = parse_input(file)
    self.reset()

  def reset(self):
    self.labels = []
    self.focal_lengths = []
    for _ in range(256):
      self.labels.append([])
      self.focal_lengths.append({})

  def perform_step(self, step):
    label, focal_length = parse_step(step)
    box = HASH(label)
    if focal_length is None:  # -
      if label in self.labels[box]:
        self.labels[box].remove(label)
      self.focal_lengths[box].pop(label, None)
    else:                     # =
      if label not in self.labels[box]:
        self.labels[box].append(label)
      self.focal_lengths[box][label] = focal_length

  def focusing_power(self, box):
    if not self.labels[box]:
      return 0
    return sum((box + 1) * i * self.focal_lengths[box][label]
               for i, label in enumerate(self.labels[box], start=1))

  def total_focusing_power(self):
    return sum(map(self.focusing_power, range(len(self.labels))))

  def run(self):
    self.reset()
    for step in self.steps:
      self.perform_step(step)
    return self.total_focusing_power()

test_steps = parse_input(TEST_INPUT_FILE)
assert sum(map(HASH, test_steps)) == 1320
test_boxes = Boxes(TEST_INPUT_FILE)
assert test_boxes.run() == 145

real_steps = parse_input(INPUT_FILE)
print(f'Day {DAY} part 1: {sum(map(HASH, real_steps))}')
real_boxes = Boxes(INPUT_FILE)
print(f'Day {DAY} part 2: {real_boxes.run()}')
