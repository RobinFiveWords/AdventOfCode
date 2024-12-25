

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'


def parse_input(file):
  with open(file) as f:
    sections = f.read().strip().split('\n\n')
  keys = []
  locks = []
  for section in sections:
    lines = section.split('\n')
    heights = [0, 0, 0, 0, 0]
    if lines[0][0] == '#':  
      # lock
      for i, line in enumerate(lines[1:-1], start=1):
        for j, char in enumerate(line):
          if char == '#':
            heights[j] = i
      locks.append(heights)
    else:
      # key
      for i, line in enumerate(lines[1:-1][::-1], start=1):
        for j, char in enumerate(line):
          if char == '#':
            heights[j] = i
      keys.append(heights)
  return keys, locks


def count_fits(keys, locks):
  return sum(all(k + l <= 5 for k, l in zip(key, lock))
             for key in keys for lock in locks)


def main():
  print(f'Day {DAY} part 1: {count_fits(*parse_input(INPUT_FILE))}')
  # print(f'Day {DAY} part 2: {}')
  pass

if __name__ == '__main__':
  main()
