import re

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

regex_mul = re.compile(r"mul\((\d+),(\d+)\)")
regex_do = re.compile(r"do\(\)")
regex_dont = re.compile(r"don't\(\)")

def parse_input(file):
  with open(file) as f:
    return f.read()

def part1(s):
  return sum(map(lambda x: int(x[0]) * int(x[1]), regex_mul.findall(s)))

def part2(s):
  muls = [(m.start(), "mul", m.groups()) for m in regex_mul.finditer(s)]
  dos = [(m.start(), "do", None) for m in regex_do.finditer(s)]
  donts = [(m.start(), "don't", None) for m in regex_dont.finditer(s)]
  instructions = sorted(muls + dos + donts)
  do = True
  result = 0
  for _, op, vals in instructions:
    if op == "do":
      do = True
    elif op == "don't":
      do = False
    elif op == "mul" and do:
      result += int(vals[0]) * int(vals[1])
  return result

def main():
  print(f'Day {DAY} part 1: {part1(parse_input(INPUT_FILE))}')
  print(f'Day {DAY} part 2: {part2(parse_input(INPUT_FILE))}')
  pass

if __name__ == '__main__':
  main()
