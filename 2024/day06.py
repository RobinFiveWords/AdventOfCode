from aoc import Point, Up, Down, Left, Right

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

DIRECTIONS = [Up, Right, Down, Left]

class Lab:
  def __init__(self, file):
    self.walls = set()
    self.start = None
    with open(file) as f:
      for y, line in enumerate(f.read().strip().split('\n')):
        for x, char in enumerate(line):
          if char == '#':
            self.walls.add(Point(x, y))
          elif char == '^':
            self.start = Point(x, y)
    self.xmax = x
    self.ymax = y

  def walk(self):
    visited = set()
    direction_index = 0
    current = self.start
    while 0 <= current.x <= self.xmax and 0 <= current.y <= self.ymax:
      visited.add(current)
      if (step := current + DIRECTIONS[direction_index % 4]) not in self.walls:
        current = step
      else:
        direction_index += 1
    return len(visited)

  def obstruct(self, point):
    if point in self.walls or point == self.start:
      return False
    obstructions = self.walls.copy()
    obstructions.add(point)
    direction_index = 0
    current = (self.start, DIRECTIONS[direction_index])
    positions = set()
    positions.add(current)
    while True:
      location, direction = current
      if location.x < 0 or location.x > self.xmax \
          or location.y < 0 or location.y > self.ymax:
        return False
      if (step := location + direction) not in obstructions:
        current = (step, direction)
      else:
        direction_index += 1
        current = (location, DIRECTIONS[direction_index % 4])
      if current in positions:
        return True
      positions.add(current)

  def search(self):
    return sum(self.obstruct(Point(x, y))
               for x in range(self.xmax + 1)
               for y in range(self.ymax + 1))

# Part 2 took two minutes to finish.
# I imagine I could make it faster by jumping to the obstruction
# rather than taking one step at a time.

def main():
  print(f'Day {DAY} part 1: {Lab(INPUT_FILE).walk()}')
  print(f'Day {DAY} part 2: {Lab(INPUT_FILE).search()}')
  pass

if __name__ == '__main__':
  main()
