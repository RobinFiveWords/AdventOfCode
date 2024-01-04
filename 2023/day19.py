import operator
import re

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

RULE = re.compile(r'([xmas])([<>])(\d+):(\w+)')
OPERATORS = {'>': operator.gt, '<': operator.lt}

class Part:
  def __init__(self, s):
    self.x, self.m, self.a, self.s = parse_ints(s)

  def score(self):
    return self.x + self.m + self.a + self.s

  def __repr__(self):
    return f"Part(x={self.x},m={self.m},a={self.a},s={self.s})"

class Workflow:
  def __init__(self, s):
    self.name, rules = s[:-1].split('{')
    self.rules = []
    for rule in rules.split(','):
      match = RULE.match(rule)
      if match:
        category = match.group(1)
        op = OPERATORS[match.group(2)]
        comparison = int(match.group(3))
        destination = match.group(4)
        self.rules.append([category, op, comparison, destination])
      else:
        self.rules.append([rule])

  def run(self, part):
    for rule in self.rules:
      if len(rule) == 1:  # last rule
        return rule[0]
      category, op, comparison, destination = rule
      if op(getattr(part, category), comparison):
        return destination

class Workflows:
  def __init__(self, file):
    with open(file) as f:
      flows, parts = f.read().strip().split('\n\n')
    self.workflows = {}
    for flow in flows.split('\n'):
      workflow = Workflow(flow)
      self.workflows[workflow.name] = workflow
    self.parts = [Part(part) for part in parts.split('\n')]
    self.results = []

  def run(self):
    self.results.clear()
    for part in self.parts:
      current = 'in'
      while current in self.workflows:
        current = self.workflows[current].run(part)
      if current == 'A':
        self.results.append(True)
      elif current == 'R':
        self.results.append(False)
      else:
        raise ValueError(f'{part} reached unexpected workflow {current}')
    return self.score()

  def score(self):
    return sum(part.score() for i, part in enumerate(self.parts)
               if self.results[i])


class Workflows2:
  def __init__(self, file):
    with open(file) as f:
      flows, parts = f.read().strip().split('\n\n')
    self.workflows = {}
    for flow in flows.split('\n'):
      workflow = Workflow(flow)
      self.workflows[workflow.name] = workflow
    self.results = []
    self.pending = []

    self.destination = None
    self.xmin = None
    self.xmax = None
    self.mmin = None
    self.mmax = None
    self.amin = None
    self.amax = None
    self.smin = None
    self.smax = None

  def analyze(self):
    new_ranges = (self.xmin, self.xmax,
                  self.mmin, self.mmax,
                  self.amin, self.amax,
                  self.smin, self.smax)
    if self.destination == 'A':
      # print(f'*** ACCEPTED: {new_ranges} ***')
      self.results.append(new_ranges)
    elif self.destination == 'R':
      # print(f'!!! REJECTED: {new_ranges} !!!')
      pass
    else:
      new_state = (self.destination, new_ranges)
      # print(new_state)
      self.pending.append(new_state)

  def run(self):
    self.results.clear()
    starting_ranges = (1, 4000) * 4
    starting_state = ('in', starting_ranges)
    current = [starting_state]
    while current:
      for name, ranges in current:
        # print(name)
        workflow = self.workflows[name]
        (self.xmin, self.xmax,
         self.mmin, self.mmax,
         self.amin, self.amax,
         self.smin, self.smax) = ranges
        for rule in workflow.rules:
          # print(rule)
          if len(rule) == 1:  # last rule
            self.destination = rule[0]
            self.analyze()
          else:
            category, op, comparison, self.destination = rule

            if op == operator.gt:
              if category == 'x':
                if self.xmax <= comparison:  # no part of range sent to destination
                  continue
                elif self.xmin > comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_xmin = self.xmin
                  next_xmax = comparison
                  self.xmin = comparison + 1
                  self.analyze()
                  self.xmin = next_xmin
                  self.xmax = next_xmax
              elif category == 'm':
                if self.mmax <= comparison:  # no part of range sent to destination
                  continue
                elif self.mmin > comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_mmin = self.mmin
                  next_mmax = comparison
                  self.mmin = comparison + 1
                  self.analyze()
                  self.mmin = next_mmin
                  self.mmax = next_mmax
              elif category == 'a':
                if self.amax <= comparison:  # no part of range sent to destination
                  continue
                elif self.amin > comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_amin = self.amin
                  next_amax = comparison
                  self.amin = comparison + 1
                  self.analyze()
                  self.amin = next_amin
                  self.amax = next_amax
              elif category == 's':
                if self.smax <= comparison:  # no part of range sent to destination
                  continue
                elif self.smin > comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_smin = self.smin
                  next_smax = comparison
                  self.smin = comparison + 1
                  self.analyze()
                  self.smin = next_smin
                  self.smax = next_smax
              else:
                raise ValueError(f'Unknown category {category}')

            else:  # op == operator.lt
              if category == 'x':
                if self.xmin >= comparison:  # no part of range sent to destination
                  continue
                elif self.xmax < comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_xmin = comparison
                  next_xmax = self.xmax
                  self.xmax = comparison - 1
                  self.analyze()
                  self.xmin = next_xmin
                  self.xmax = next_xmax
              elif category == 'm':
                if self.mmin >= comparison:  # no part of range sent to destination
                  continue
                elif self.mmax < comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_mmin = comparison
                  next_mmax = self.mmax
                  self.mmax = comparison - 1
                  self.analyze()
                  self.mmin = next_mmin
                  self.mmax = next_mmax
              elif category == 'a':
                if self.amin >= comparison:  # no part of range sent to destination
                  continue
                elif self.amax < comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_amin = comparison
                  next_amax = self.amax
                  self.amax = comparison - 1
                  self.analyze()
                  self.amin = next_amin
                  self.amax = next_amax
              elif category == 's':
                if self.smin >= comparison:  # no part of range sent to destination
                  continue
                elif self.smax < comparison:  # entire range sent to destination
                  self.analyze()
                else:  # split range
                  next_smin = comparison
                  next_smax = self.smax
                  self.smax = comparison - 1
                  self.analyze()
                  self.smin = next_smin
                  self.smax = next_smax
              else:
                raise ValueError(f'Unknown category {category}')

      current = self.pending[:]
      self.pending.clear()


def volume4d(hypercube):
  x1, x2, m1, m2, a1, a2, s1, s2 = hypercube
  return (x2 - x1 + 1) * (m2 - m1 + 1) * (a2 - a1 + 1) * (s2 - s1 + 1)

test_workflows = Workflows(TEST_INPUT_FILE)
assert test_workflows.run() == 19114
test_workflows2 = Workflows2(TEST_INPUT_FILE)
test_workflows2.run()
assert sum(map(volume4d, test_workflows2.results)) == 167409079868000

real_workflows = Workflows(INPUT_FILE)
print(f'Day {DAY} part 1: {real_workflows.run()}')
real_workflows2 = Workflows2(INPUT_FILE)
real_workflows2.run()
print(f'Day {DAY} part 2: {sum(map(volume4d, real_workflows2.results))}')
