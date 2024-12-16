from collections import defaultdict
from functools import cache
from heapq import heappop, heappush

from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Down, Left, Right]

OPPOSITES = {
  Up: Down,
  Right: Left,
  Down: Up,
  Left: Right,
}

TURNS = {
  Up: [Right, Left],
  Right: [Down, Up],
  Down: [Left, Right],
  Left: [Up, Down],
}

STEP = 1
TURN = 1000


class Maze:
  def __init__(self, file):
    with open(file) as f:
      lines = f.read().strip().split('\n')
    self.tiles = set()
    self.start = None
    self.end = None
    for y, line in enumerate(lines):
      for x, char in enumerate(line):
        if char == '#':
          continue
        point = Point(x, y)
        self.tiles.add(point)
        if char == 'S':
          self.start = point
        elif char == 'E':
          self.end = point
    self.adj = defaultdict(set)
    for p1 in self.tiles:
      for direction in DIRECTIONS:
        p2 = p1 + direction
        if p2 in self.tiles:
          self.adj[p1].add(p2)
          self.adj[p2].add(p1)
    self.nodes = sorted(p for p, a in self.adj.items()
                        if p in [self.start, self.end] or len(a) > 2)
    self.connections = defaultdict(lambda: defaultdict(list))
    # connection -> (direction in, direction out, score)
    for node in self.nodes:
      for neighbor in self.adj[node]:
        previous_loc = node
        current_loc = neighbor
        direction_in = current_loc - previous_loc
        current_dir = direction_in
        score = STEP
        valid = True
        while current_loc not in self.nodes:
          next_loc = [n for n in self.adj[current_loc]
                      if n != previous_loc]
          if not next_loc:
            valid = False
            break
          assert len(next_loc) == 1
          previous_loc = current_loc
          current_loc = next_loc[0]
          score += STEP
          next_dir = current_loc - previous_loc
          if next_dir != current_dir:
            score += TURN
          current_dir = next_dir
        if valid:
          self.connections[node][current_loc].append((direction_in, current_dir, score))

  @cache
  def h(self, point):
    return self.end.manhattan_distance(point)

  def search(self):
    # priority queue item -> (total + heuristic, (total, current_loc, current_dir))
    pq = []
    best = float('+inf')
    visited = {}
    score = 0
    current_loc = self.start
    current_dir = Right
    heappush(pq, (score, (score, current_loc, current_dir)))
    while pq:
      total_plus_h, (total, current_loc, current_dir) = heappop(pq)
      if total_plus_h >= best:
        return best
      for next_loc, options in self.connections[current_loc].items():
        for dir_in, next_dir, score in options:
          if dir_in == current_dir:
            pass  # continue straight
          elif dir_in in TURNS[current_dir]:
            score += TURN
          else:
            continue  # no need to double back
          next_total = total + score
          if next_loc == self.end:
            if next_total < best:
              best = next_total
          if visited.get((next_loc, next_dir), float('inf')) < next_total:
            continue
          visited[(next_loc, next_dir)] = next_total
          h = self.h(next_loc)
          heappush(pq, (next_total + h, (next_total, next_loc, next_dir)))

  def search2(self):
    # priority queue item -> (total + heuristic, (total, current_loc, current_dir, path_dir_outs))
    pq = []
    best = float('+inf')
    best_paths = []
    visited = {}
    score = 0
    current_loc = self.start
    current_dir = Right
    heappush(pq, (score, (score, current_loc, current_dir, [])))
    while pq:
      total_plus_h, (total, current_loc, current_dir, path_dir_outs) = heappop(pq)
      if total_plus_h > best:
        break
      for next_loc, options in self.connections[current_loc].items():
        for dir_in, next_dir, score in options:
          if dir_in == current_dir:
            pass  # continue straight
          elif dir_in in TURNS[current_dir]:
            score += TURN
          else:
            continue  # no need to double back
          next_total = total + score
          next_path_dir_outs = path_dir_outs[:] + [next_dir]
          if next_loc == self.end:
            if next_total < best:
              best = next_total
              best_paths = [next_path_dir_outs]
            elif next_total == best:
              best_paths.append(next_path_dir_outs)
          if visited.get((next_loc, next_dir), float('inf')) < next_total:
            continue
          visited[(next_loc, next_dir)] = next_total
          h = self.h(next_loc)
          heappush(pq, (next_total + h, (next_total, next_loc, next_dir, next_path_dir_outs)))
    best_tiles = set([self.end])
    for path in best_paths:
      current = self.end
      directions = [OPPOSITES[direction] for direction in reversed(path)]
      for direction in directions:
        previous = current
        current += direction
        best_tiles.add(current)
        while current not in self.nodes:
          next_loc = [n for n in self.adj[current] if n != previous][0]
          previous = current
          current = next_loc
          best_tiles.add(current)
    return len(best_tiles)


def main():
  print(f'Day {DAY} part 1: {Maze(INPUT_FILE).search()}')
  print(f'Day {DAY} part 2: {Maze(INPUT_FILE).search2()}')
  pass

if __name__ == '__main__':
  main()
