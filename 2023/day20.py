import collections
import math

from aoc import flatten

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')
TEST_INPUT_FILE2 = INPUT_FILE.replace('input', 'testinput2')

class FlipFlop:
  def __init__(self, queue, name, destinations):
    self.queue = queue
    self.name = name
    self.destinations = destinations
    self.on = False

  def update(self, pulse):
    level, _, _ = pulse
    if not level:
      self.on = not self.on
      for destination in self.destinations:
        pulse = (self.on, destination, self.name)
        self.queue.append(pulse)

  def state(self):
    return self.on

  def __repr__(self):
    return f"FlipFlop({self.name} -> {', '.join(self.destinations)})"


class Conjunction:
  def __init__(self, queue, name, destinations, sources):
    self.queue = queue
    self.name = name
    self.destinations = destinations
    self.sources = {source: False for source in sources}

  def update(self, pulse):
    level, _, source = pulse
    self.sources[source] = level
    if all(self.sources.values()):
      for destination in self.destinations:
        pulse = (False, destination, self.name)
        self.queue.append(pulse)
    else:
      for destination in self.destinations:
        pulse = (True, destination, self.name)
        self.queue.append(pulse)
      return self.name

  def state(self):
    return tuple(self.sources.values())

  def __repr__(self):
    return f"Conjunction({self.name} -> {', '.join(self.destinations)})"


class Broadcaster:
  def __init__(self, queue, name, destinations):
    self.queue = queue
    self.name = name
    self.destinations = destinations

  def update(self, pulse):
    level, _, _ = pulse
    for destination in self.destinations:
      pulse = (level, destination, self.name)
      self.queue.append(pulse)

  def state(self):
    return False

  def __repr__(self):
    return f"Broadcaster({self.name} -> {', '.join(self.destinations)})"


class System:
  def __init__(self, file):
    with open(file) as f:
      self.lines = f.read().strip().split('\n')
    self.destinations = collections.defaultdict(list)
    self.sources = collections.defaultdict(list)
    for line in self.lines:
      source, ds = line.split(' -> ')
      if source != 'broadcaster':
        source = source[1:]
      for destination in ds.split(', '):
        self.destinations[source].append(destination)
        self.sources[destination].append(source)

    self.modules = {}
    self.queue = collections.deque()
    for line in self.lines:
      module = line.split()[0]
      if module[0] == '%':
        self.modules[module[1:]] = FlipFlop(self.queue,
                                            module[1:],
                                            self.destinations[module[1:]])
      elif module[0] == '&':
        self.modules[module[1:]] = Conjunction(self.queue,
                                               module[1:],
                                               self.destinations[module[1:]],
                                               self.sources[module[1:]])
      else:
        self.modules[module] = Broadcaster(self.queue,
                                           module,
                                           self.destinations[module])
    self.low_pulses = [0]
    self.high_pulses = [0]
    self.button_pushes = 0

    # there are four components feeding into &nr
    self.nr_sources = set(self.sources['nr'])
    self.sends_high = collections.defaultdict(set)

  def push_button(self):
    self.button_pushes += 1
    pulse = (False, 'broadcaster', 'button')
    self.queue.append(pulse)
    pulses = collections.Counter()
    while self.queue:
      pulse = self.queue.popleft()
      level, destination, source = pulse
      pulses[level] += 1
      if destination in self.modules:
        result = self.modules[destination].update(pulse)
      if result in self.nr_sources:
        self.sends_high[result].add(self.button_pushes)
    self.low_pulses.append(pulses[False])
    self.high_pulses.append(pulses[True])

  def run(self, N=10000):
    while self.button_pushes < N:
      self.push_button()

  def multiply(self, N=1000):
    return sum(self.low_pulses[:N+1]) * sum(self.high_pulses[:N+1])

  def low_rx(self):
    # testing showed each is a cycle starting from 0
    return math.lcm(*(min(v) for v in self.sends_high.values()))

t1 = System(TEST_INPUT_FILE)
t1.run()
assert t1.multiply() == 32000000
t2 = System(TEST_INPUT_FILE2)
t2.run()
assert t2.multiply() == 11687500

r = System(INPUT_FILE)
r.run()
print(f'Day {DAY} part 1: {r.multiply()}')
print(f'Day {DAY} part 2: {r.low_rx()}')
