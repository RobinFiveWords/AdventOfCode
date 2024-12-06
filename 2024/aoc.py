#!/usr/bin/env python
# aoc.py
# for Advent of Code 2020

import collections
import re


regex_digits = re.compile(r'\d+')
regex_digits_negative = re.compile(r'\-?\d+')


P = collections.namedtuple('Point', ['x', 'y'])

class Point(P):
  def __add__(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def __mul__(self, value):
    return Point(self.x * value, self.y * value)

  def manhattan_distance(self, other):
    return abs(self.x - other.x) + abs(self.y - other.y)

Origin = Point( 0,  0)
Up     = Point( 0, -1)
Down   = Point( 0,  1)
Left   = Point(-1,  0)
Right  = Point( 1,  0)


def display_points(points):
  xmin = min(p.x for p in points)
  xmax = max(p.x for p in points)
  ymin = min(p.y for p in points)
  ymax = max(p.y for p in points)
  for y in range(ymin, ymax + 1):
    for x in range(xmin, xmax + 1):
      if Point(x, y) in points:
        print('#', end='')
      else:
        print('.', end='')
    print()


def flatten(L):
    """Recursively flatten iterables while treating strings as atoms."""
    for item in L:
        if isinstance(item, str):
            yield item
        else:
            try:
                yield from flatten(item)
            except TypeError:
                yield item


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
assert manhattan_distance((1, 2), (3, 4)) == 4
assert manhattan_distance((1, 1), (-1, 1)) == 2


def parse_ints(s, negative=False):
  if negative:
    return [int(n) for n in regex_digits_negative.findall(s)]
  return [int(n) for n in regex_digits.findall(s)]


def sign(x): return (x > 0) - (x < 0)
assert [sign(x) for x in [-2, -1, 0, 1, 2]] == [-1, -1, 0, 1, 1]

def single(vals):
  if isinstance(vals, map):
    vals = list(vals)
  unique = set(vals)
  assert len(unique) == 1, f'expecting exactly one value but received {vals}'
  return unique.pop()
