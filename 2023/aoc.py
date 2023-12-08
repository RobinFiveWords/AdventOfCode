#!/usr/bin/env python
# aoc.py
# for Advent of Code 2023

import collections
import math
import re
import sympy


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


def lcm(integers):
  prime_factors = collections.Counter()
  for n in integers:
    prime_factors |= sympy.factorint(n)
  return math.prod(factor ** exponent
                   for factor, exponent in prime_factors.items())


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
