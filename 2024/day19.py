from functools import cache
import re

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'


class Analysis:
  def __init__(self, file):
    with open(file) as f:
      sections = f.read().strip().split('\n\n')
    self.patterns = sorted(sections[0].split(', '), key=lambda s: len(s))
    assert len(self.patterns) == len(set(self.patterns))
    self.min_pattern_length = min(map(len, self.patterns))
    self.max_pattern_length = max(map(len, self.patterns))
    self.designs = sections[1].split('\n')
    self.cleaned_patterns = self.clean()
    self.regex = re.compile(r'^(' + '|'.join(self.cleaned_patterns) + ')+$')

  def clean(self):
    working = [p for p in self.patterns if len(p) == self.min_pattern_length]
    for pattern in self.patterns[len(working):]:  # those longer than min length
      regex = re.compile(r'^(' + '|'.join(working) + ')+$')
      if not regex.match(pattern):
        working.append(pattern)
    return working

  def count_valid(self):
    result = 0
    number = 0
    for design in self.designs:
      number += 1
      match = self.regex.match(design)
      if match:
        result += 1
    return result

  @cache
  def ways(self, s):
    result = 0
    if s in self.patterns:
      result += 1
    for length in range(self.min_pattern_length, self.max_pattern_length + 1):
      if s[:length] in self.patterns:
        result += self.ways(s[length:])
    return result

  def count_ways(self):
    return sum(self.ways(design) for design in self.designs)


def main():
  print(f'Day {DAY} part 1: {Analysis(INPUT_FILE).count_valid()}')
  print(f'Day {DAY} part 2: {Analysis(INPUT_FILE).count_ways()}')
  pass

if __name__ == '__main__':
  main()
