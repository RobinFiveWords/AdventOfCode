import math

OPERATIONS = {
  '+': sum,
  '*': math.prod,
}

def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  args = list(zip(*[[int(n) for n in line.split()] for line in lines[:-1]]))
  operations = [OPERATIONS[op] for op in lines[-1].split()]
  return args, operations

def aggregate(args, operations, aggfunc=sum):
  return aggfunc(op(a) for a, op in zip(args, operations))

assert aggregate(*parse_file('testinput06.txt')) == 4277556


def parse_file2(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  columns = []
  for _ in range(max(len(line) for line in lines)):
    columns.append([])  # because [[]] * val -> copies of a single list
  for line in lines[:-1]:
    for i, char in enumerate(line):
      columns[i].append(char)
  for i in range(len(columns)):
    columns[i] = ''.join(columns[i]).replace(' ', '')
  args = []
  working = []
  for column in columns:
    if not column:
      args.append(tuple(working))
      working.clear()
    else:
      working.append(int(column))
  if working:
    args.append(tuple(working))
  operations = [OPERATIONS[op] for op in lines[-1].split()]
  return args, operations


assert aggregate(*parse_file2('testinput06.txt')) == 3263827


print('Day 6 part 1:', aggregate(*parse_file('input06.txt')))
print('Day 6 part 2:', aggregate(*parse_file2('input06.txt')))
