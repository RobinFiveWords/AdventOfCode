from collections import Counter


def parse_file(file):
  with open(file) as f:
    lines = f.read().strip().split('\n')
  adj = {}
  for line in lines:
    tokens = line.split()
    adj[tokens[0][:-1]] = tokens[1:]
  return adj


def count_paths(adj, start='you', end='out'):
  assert start != end
  result = 0
  current = Counter({start: 1})
  pending = Counter()
  while current:
    for node, count in current.items():
      for next_node in adj[node]:
        if next_node == end:
          result += count
        else:
          pending[next_node] += count
    current = pending.copy()
    pending.clear()
  return result


def count_paths2(adj):
  result = 0
  current = Counter({('svr', False, False): 1})
  pending = Counter()
  while current:
    for (node, dac, fft), count in current.items():
      for next_node in adj[node]:
        if next_node == 'out':
          if dac and fft:
            result += count
        else:
          next_dac = dac or next_node == 'dac'
          next_fft = fft or next_node == 'fft'
          pending[(next_node, next_dac, next_fft)] += count
    current = pending.copy()
    pending.clear()
  return result


assert count_paths(parse_file('testinput11.txt')) == 5
assert count_paths2(parse_file('testinput11b.txt')) == 2


print('Day 11 part 1:', count_paths(parse_file('input11.txt')))
print('Day 11 part 2:', count_paths2(parse_file('input11.txt')))

# #1117 for part 1
# #496 for part 2
