from fractions import Fraction

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

BIG_N = 10000000000000

def parse_input(file):
  with open(file) as f:
    return [parse_ints(section) for section in f.read().strip().split('\n\n')]

def brute_force_cost(machine):
  # brute force
  xa, ya, xb, yb, xp, yp = machine
  for b in range(yp // yb, -1, -1):
    x = xp - b * xb
    y = yp - b * yb
    for a in range(x // xa, -1, -1):
      result = check(machine, a, b)
      if result:
        return 3 * a + b
  return 0

def check(machine, a, b):
  xa, ya, xb, yb, xp, yp = machine
  return (a * xa + b * xb == xp) and (a * ya + b * yb == yp)

def cost(machine, offset=0):
  assert len(machine) == 6
  assert all(n > 0 for n in machine)
  xa, ya, xb, yb, xp, yp = machine
  assert Fraction(ya, xa) != Fraction(yb, xb)
  xp += offset
  yp += offset
  # a bunch of algebra to find intersection of lines through
  # Origin with slope A and Prize with slope B
  x = Fraction(Fraction(xp * yb, xb) - yp, Fraction(yb, xb) - Fraction(ya, xa))
  a = Fraction(x, xa)
  b = Fraction(xp - x, xb)
  if int(a) != a or int(b) != b:
    return 0
  return int(3 * a + b)

def total_cost(machines, offset=0):
  return sum(cost(machine, offset) for machine in machines)

def main():
  machines = parse_input(INPUT_FILE)
  print(f'Day {DAY} part 1: {total_cost(machines)}')
  print(f'Day {DAY} part 2: {total_cost(machines, BIG_N)}')
  pass

if __name__ == '__main__':
  main()
