from collections import defaultdict

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

ops = {'AND': 1, 'OR': 2, 'XOR': 3}


class Wires:
  def __init__(self, file):
    with open(file) as f:
      starting, wires = f.read().strip().split('\n\n')
    self.output = {}
    for line in starting.split('\n'):
      tokens = line.split(': ')
      self.output[tokens[0]] = int(tokens[1])
    self.wires = {}
    for line in wires.split('\n'):
      i, op, j, _, out = line.split()
      self.wires[out] = (i, j, op)
    self.adj = defaultdict(dict)
    for out, (i, j, op) in self.wires.items():
      self.adj[i][out] = ops[op]
      self.adj[j][out] = ops[op]

  def evaluate(self):
    current = list(self.wires)
    pending = []
    while current:
      for wire in current:
        i, j, op = self.wires[wire]
        if i not in self.output or j not in self.output:
          pending.append(wire)
          continue
        if op == 'AND':
          self.output[wire] = self.output[i] & self.output[j]
        elif op == 'OR':
          self.output[wire] = self.output[i] | self.output[j]
        elif op == 'XOR':
          self.output[wire] = self.output[i] ^ self.output[j]
        else:
          raise ValueError(f'unrecognized operation {op}')
      current = pending
      pending = []
    return self.number()

  def number(self, prefix='z'):
    pairs = sorted((k, v) for k, v in self.output.items() if k.startswith(prefix))
    bits = ''.join(str(v) for k, v in reversed(pairs))
    return int(bits, 2)


def main():
  print(f'Day {DAY} part 1: {Wires(INPUT_FILE).evaluate()}')
  # print(f'Day {DAY} part 2: {}')
  pass

if __name__ == '__main__':
  main()
