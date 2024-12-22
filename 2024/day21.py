from collections import Counter, defaultdict
import itertools

from aoc import parse_ints

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

opposites = {
  '^': 'v',
  '>': '<',
  'v': '^',
  '<': '>',
}

def parse_instructions(instructions):
  output = defaultdict(dict)
  lines = instructions.strip().split('\n')
  for line in lines:
    tokens = line.replace(' to ', ',').replace(': ', ',').replace(' or ', ',').split(',')
    f, t = tokens[:2]
    ways = tokens[2:]
    output[f][t] = ways
    reversed_ways = []
    for way in ways:
      reversed_way = []
      temp_way = way[-2::-1] + way[-1]
      for char in temp_way:
        reversed_way.append(opposites.get(char, char))
      reversed_ways.append(''.join(reversed_way))
    output[t][f] = reversed_ways
  for k in output:
    output[k][k] = ['A']
  return output

directional_instructions = """
A to <: v<<A
A to ^: <A
A to >: vA
A to v: <vA or v<A
^ to <: v<A
^ to v: vA
^ to >: v>A or >vA
< to v: >A
< to >: >>A
v to >: >A
"""
directional = parse_instructions(directional_instructions)

numeric_instructions = """
A to 0: <A
A to 1: ^<<A or <^<A
A to 2: <^A or ^<A
A to 3: ^A
A to 4: ^^<<A or ^<<^A or <^^<A
A to 5: <^^A or ^^<A
A to 6: ^^A
A to 7: ^<<^^A or ^^^<<A or <^^^<A
A to 8: <^^^A or ^^^<A
A to 9: ^^^A
0 to 1: ^<A
0 to 2: ^A
0 to 3: >^A or ^>A
0 to 4: ^^<A or ^<^A
0 to 5: ^^A
0 to 6: >^^A or ^^>A
0 to 7: ^^^<A or ^<^^A
0 to 8: ^^^A
0 to 9: >^^^A or ^^^>A
1 to 2: >A
1 to 3: >>A
1 to 4: ^A
1 to 5: >^A or ^>A
1 to 6: >>^A or ^>>A
1 to 7: ^^A
1 to 8: >^^A or ^^>A
1 to 9: >>^^A or ^^>>A
2 to 3: >A
2 to 4: <^A or ^>A
2 to 5: ^A
2 to 6: >^A or ^>A
2 to 7: <^^A or ^^<A
2 to 8: ^^A
2 to 9: >^^A or ^^>A
3 to 4: <<^A or ^<<A
3 to 5: <^A or ^<A
3 to 6: ^A
3 to 7: <<^^A or ^^<<A
3 to 8: <^^A or ^^<A
3 to 9: ^^A
4 to 5: >A
4 to 6: >>A
4 to 7: ^A
4 to 8: >^A or ^>A
4 to 9: >>^A or ^^>A
5 to 6: >A
5 to 7: <^A or ^<A
5 to 8: ^A
5 to 9: >^A or ^>A
6 to 7: <<^A or ^<<A
6 to 8: <^A or ^<A
6 to 9: ^A
7 to 8: >A
7 to 9: >>A
8 to 9: >A
"""
numeric = parse_instructions(numeric_instructions)

def next_level(s, d, start='A'):
  lists = []
  _from = start
  for _to in s:
    lists.append(d[_from][_to])
    _from = _to
  return set(''.join(p) for p in itertools.product(*lists))

def complexity(code):
  x1 = next_level(code, numeric)
  x2 = set(itertools.chain.from_iterable(next_level(s, directional) for s in x1))
  x3 = set(itertools.chain.from_iterable(next_level(s, directional) for s in x2))
  return parse_ints(code)[0] * min(map(len, x3))

def parse_input(file):
  with open(file) as f:
    return f.read().strip().split('\n')

def expand_instr_2(instr):
  output = defaultdict(Counter)
  for line in instr.strip().split('\n'):
    _from, _to, steps = line.split()
    start = _from + _to
    for i in range(len(steps) - 1):
      key = steps[i:i+2]
      output[start][key] += 1
  return output

d_instr_2 = """
A A AA
A ^ A<A
A < Av<<A
A v A<vA
A > AvA
^ A A>A
^ ^ AA
^ < Av<A
^ v AvA
^ > Av>A
< A A>>^A
< ^ A>^A
< < AA
< v A>A
< > A>>A
v A A^>A
v ^ A^A
v < A<A
v v AA
v > A>A
> A A^A
> ^ A<^A
> < A<<A
> v A<A
> > AA
"""
d_instr_2_expanded = expand_instr_2(d_instr_2)

n_instr_2 = """
A A AA
A 0 A<A
A 1 A^<<A
A 2 A<^A
A 3 A^A
A 4 A^^<<A
A 5 A<^^A
A 6 A^^A
A 7 A^^^<<A
A 8 A<^^^A
A 9 A^^^A
0 A A>A
0 0 AA
0 1 A^<A
0 2 A^A
0 3 A^>A
0 4 A^^<A
0 5 A^^A
0 6 A^^>A
0 7 A^^^<A
0 8 A^^^A
0 9 A^^^>A
1 A A>>vA
1 0 A>vA
1 1 AA
1 2 A>A
1 3 A>>A
1 4 A^A
1 5 A^>A
1 6 A^>>A
1 7 A^^A
1 8 A^^>A
1 9 A^^>>A
2 A Av>A
2 0 AvA
2 1 A<A
2 2 AA
2 3 A>A
2 4 A<^A
2 5 A^A
2 6 A^>A
2 7 A<^^A
2 8 A^^A
2 9 A^^>A
3 A AvA
3 0 A<vA
3 1 A<<A
3 2 A<A
3 3 AA
3 4 A<<^A
3 5 A<^A
3 6 A^A
3 7 A<<^^A
3 8 A<^^A
3 9 A^^A
4 A A>>vvA
4 0 A>vvA
4 1 AvA
4 2 Av>A
4 3 Av>>A
4 4 AA
4 5 A>A
4 6 A>>A
4 7 A^A
4 8 A^>A
4 9 A^>>A
5 A Avv>A
5 0 AvvA
5 1 A<vA
5 2 AvA
5 3 Av>A
5 4 A<A
5 5 AA
5 6 A>A
5 7 A<^A
5 8 A^A
5 9 A^>A
6 A AvvA
6 0 A<vvA
6 1 A<<vA
6 2 A<vA
6 3 AvA
6 4 A<<A
6 5 A<A
6 6 AA
6 7 A<<^A
6 8 A<^A
6 9 A^A
7 A A>>vvvA
7 0 A>vvvA
7 1 AvvA
7 2 Avv>A
7 3 Avv>>A
7 4 AvA
7 5 Av>A
7 6 Av>>A
7 7 AA
7 8 A>A
7 9 A>>A
8 A Avvv>A
8 0 AvvvA
8 1 A<vvA
8 2 AvvA
8 3 Avv>A
8 4 A<vA
8 5 AvA
8 6 Av>A
8 7 A<A
8 8 AA
8 9 A>A
9 A AvvvA
9 0 A<vvvA
9 1 A<<vvA
9 2 A<vvA
9 3 AvvA
9 4 A<<vA
9 5 A<vA
9 6 AvA
9 7 A<<A
9 8 A<A
9 9 AA
"""
n_instr_2_expanded = expand_instr_2(n_instr_2)

def get_starting_counter(code, start='A'):
  output = Counter()
  s = start + code
  for i in range(len(s) - 1):
    output[s[i:i+2]] += 1
  return output

def next_level_expanded(c, d_exp):
  output = Counter()
  for key_in, frequency_in in c.items():
    for key_out, frequency_out in d_exp[key_in].items():
      output[key_out] += frequency_in * frequency_out
  return output

def complexity2(code, directional_robots=25):
  c = get_starting_counter(code)
  working = next_level_expanded(c, n_instr_2_expanded)
  for _ in range(directional_robots):
    working = next_level_expanded(working, d_instr_2_expanded)
  return parse_ints(code)[0] * sum(working.values())

def main():
  print(f'Day {DAY} part 1: {sum(map(complexity, parse_input(INPUT_FILE)))}')
  print(f'Day {DAY} part 2: {sum(map(complexity2, parse_input(INPUT_FILE)))}')
  pass

if __name__ == '__main__':
  main()
