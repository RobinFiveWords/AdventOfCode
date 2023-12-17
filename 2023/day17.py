import collections
import heapq
import numpy as np

from aoc import Point, Up, Down, Left, Right, Origin

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')
TEST_INPUT_FILE2 = INPUT_FILE.replace('input', 'testinput2')

CHANGES = {
  Up: [Left, Right],
  Down: [Left, Right],
  Left: [Up, Down],
  Right: [Up, Down],
}

# heuristic - probably manhattan distance?

# state - store as (point, direction, remaining moves)
# when adding (p, d, 2) to dict of visited states with min heat loss,
# also add (p, d, 1) and (p, d, 0) because they have fewer options


def parse_input(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  arr = np.zeros((len(lines), len(lines[0])), dtype=np.int32)
  for row, line in enumerate(lines):
    for col, digit in enumerate(line):
      arr[row, col] = int(digit)
  return arr  # my Point class has x across and y down; does this affect solution?


State = collections.namedtuple("State",
                               ['heat', 'point', 'direction', 'remaining'])
def PDR(state): return state.point, state.direction, state.remaining

class A_star:
  def __init__(self, file):
    self.arr = parse_input(file)
    self.xmax = self.arr.shape[0] - 1
    self.ymax = self.arr.shape[1] - 1
    self.goal = Point(self.xmax, self.ymax)

  def solve(self, prune=5000):
    pq = []
    visited = set()
    initial_states = [State(self.arr[direction], direction, direction, 2)
                      for direction in [Right, Down]]
    for state in initial_states:
      heapq.heappush(pq, (state.heat + self.heuristic(state), state))
    while pq:
      state = heapq.heappop(pq)[1]
      pdr = PDR(state)
      if pdr in visited:
        continue
      if state.point == self.goal:
        return state.heat
      visited.add(pdr)
      for remaining in range(state.remaining):
        visited.add((state.point, state.direction, remaining))
      next_states = []
      for new_direction in CHANGES[state.direction]:
        new_point = state.point + new_direction
        if not (0 <= new_point.x <= self.xmax and 0 <= new_point.y <= self.ymax):
          continue
        next_states.append(State(state.heat + self.arr[new_point.x, new_point.y],
                                 new_point,
                                 new_direction,
                                 2))
      if state.remaining > 0:
        new_point = state.point + state.direction
        if (0 <= new_point.x <= self.xmax and 0 <= new_point.y <= self.ymax):
          next_states.append(State(state.heat + self.arr[new_point.x, new_point.y],
                                   new_point,
                                   state.direction,
                                   state.remaining - 1))
      for state in next_states:
        heapq.heappush(pq, (state.heat + self.heuristic(state), state))
      pq = pq[:prune]

  def solve2(self, prune=20000):
    pq = []
    visited = set()
    initial_states = []
    for direction in [Right, Down]:
      point = Origin
      heat = 0
      for _ in range(4):
        point += direction
        heat += self.arr[point.x, point.y]
      initial_states.append(State(heat, point, direction, 6))
    for state in initial_states:
      heapq.heappush(pq, (state.heat + self.heuristic(state), state))
    while pq:
      state = heapq.heappop(pq)[1]
      pdr = PDR(state)
      if pdr in visited:
        continue
      if state.point == self.goal:
        return state.heat
      visited.add(pdr)
      next_states = []
      for remaining in range(state.remaining):
        visited.add((state.point, state.direction, remaining))
      for new_direction in CHANGES[state.direction]:
        new_point = state.point
        heat_points = []
        for _ in range(4):
          new_point += new_direction
          heat_points.append(new_point)
        if not (0 <= new_point.x <= self.xmax and 0 <= new_point.y <= self.ymax):
          continue
        new_heat = state.heat
        for point in heat_points:
          new_heat += self.arr[point.x, point.y]
        next_states.append(State(new_heat, new_point, new_direction, 6))
      if state.remaining > 0:
        new_point = state.point + state.direction
        if (0 <= new_point.x <= self.xmax and 0 <= new_point.y <= self.ymax):
          next_states.append(State(state.heat + self.arr[new_point.x, new_point.y],
                                   new_point,
                                   state.direction,
                                   state.remaining - 1))
      for state in next_states:
        heapq.heappush(pq, (state.heat + self.heuristic(state), state))
      pq = pq[:prune]

  def heuristic(self, state):
    return self.goal.manhattan_distance(state.point)

tA = A_star(TEST_INPUT_FILE)
assert tA.solve() == 102
assert tA.solve2() == 94
tA2 = A_star(TEST_INPUT_FILE2)
assert tA2.solve2() == 71

rA = A_star(INPUT_FILE)
print(f'Day {DAY} part 1: {rA.solve()}')
print(f'Day {DAY} part 2: {rA.solve2()}')
