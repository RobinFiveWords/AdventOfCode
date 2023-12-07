import itertools

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')


card_labels = '23456789TJQKA'
card_points = {label: points for points, label in enumerate(card_labels,
                                                            start=2)}

class Hand:
  def __init__(self, h):
    self.s = h.split()[0]
    self.bid = int(h.split()[1])
    self.type = self.get_type()
    self.points = [card_points[c] for c in self.s]

  def get_type(self):
    gb = itertools.groupby(sorted(self.s))
    return ''.join(str(n) for n in sorted((len(list(g)) for _, g in gb),
                                          reverse=True))

  def __lt__(self, other):
    if self.type == other.type:
      return self.points < other.points
    else:
      return self.type < other.type

  def __repr__(self):
    return f'{self.s} {self.bid}'


card_labelsJ = 'J23456789TQKA'
card_pointsJ = {label: points for points, label in enumerate(card_labelsJ,
                                                             start=1)}

class HandJ:
  def __init__(self, h):
    self.s = h.split()[0]
    self.bid = int(h.split()[1])
    self.type = self.get_type()
    self.points = [card_pointsJ[c] for c in self.s]

  def get_type(self):
    gb = itertools.groupby(sorted(self.s))
    freqs = sorted((len(list(g)) for c, g in gb if c != 'J'), reverse=True)
    Js = self.s.count('J')
    if Js == 5:
      freqs = [5]
    else:
      freqs[0] += Js
    return ''.join(str(n) for n in freqs)

  def __lt__(self, other):
    if self.type == other.type:
      return self.points < other.points
    else:
      return self.type < other.type

  def __repr__(self):
    return f'{self.s} {self.bid}'


def parse_input(file, klass):
  with open(file) as f:
    return [klass(h) for h in f.read().strip().split('\n')]


def total_winnings(hands):
  return sum(rank * hand.bid for rank, hand in enumerate(sorted(hands),
                                                         start=1))

test_hands = parse_input(TEST_INPUT_FILE, Hand)
assert total_winnings(test_hands) == 6440
test_handsJ = parse_input(TEST_INPUT_FILE, HandJ)
assert total_winnings(test_handsJ) == 5905

real_hands = parse_input(INPUT_FILE, Hand)
real_handsJ = parse_input(INPUT_FILE, HandJ)
print(f'Day {DAY} part 1: {total_winnings(real_hands)}')
print(f'Day {DAY} part 2: {total_winnings(real_handsJ)}')
