import numpy as np

DAY = int(__file__.split('/')[-1][3:5])
YEAR = int(__file__.split('/')[-2])
INPUT_FILE = f'adventofcode.com_{YEAR}_day_{DAY}_input.txt'
TEST_INPUT_FILE = INPUT_FILE.replace('input', 'testinput')

encode = {'.': 0, '#': 1}

def parse_input(file):
  with open(file) as f:
    patterns = f.read().strip().split('\n\n')
  return [parse_pattern(pattern) for pattern in patterns]

def parse_pattern(s):
  lines = s.split('\n')
  arr = np.zeros((len(lines), len(lines[0])), dtype=np.int8)
  for row, line in enumerate(lines):
    for col, char in enumerate(line):
      arr[row, col] = encode[char]
  return arr

def analyze(arr, previous=None):
  rows = arr.shape[0]
  for row in range(1, rows):
    if row > rows / 2:
      left = rows - row
      if np.array_equal(arr[rows - 2 * left:row], arr[row:][::-1]):
        result = ('r', row)
        if result != previous:
          return result
    else:
      if np.array_equal(arr[:row][::-1], arr[row:row * 2]):
        result = ('r', row)
        if result != previous:
          return result
  cols = arr.shape[1]
  for col in range(1, cols):
    if col > cols / 2:
      up = cols - col
      if np.array_equal(arr[:, cols - 2 * up:col], arr[:, col:][:, ::-1]):
        result = ('c', col)
        if result != previous:
          return result
    else:
      if np.array_equal(arr[:, :col][:, ::-1], arr[:, col:col * 2]):
        result = ('c', col)
        if result != previous:
          return result

def get_analysis(patterns):
  return {i: result for i, result in enumerate(map(analyze, patterns))}

def score(analysis):
  return sum(value * 100 if label == 'r' else value
             for label, value in analysis.values())

def reanalyze(arr, previous):
  for row in range(arr.shape[0]):
    for col in range(arr.shape[1]):
      a = arr.copy()
      a[row, col] = (a[row, col] + 1) % 2
      result = analyze(a, previous)
      if result:
        return tuple([*result, row, col])

def get_reanalysis(patterns, analysis):
  results = {}
  for i, pattern in enumerate(patterns):
    results[i] = reanalyze(pattern, analysis[i])
  return results

def rescore(reanalysis):
  return sum(value * 100 if label == 'r' else value
             for label, value, row, col in reanalysis.values())

test_patterns = parse_input(TEST_INPUT_FILE)
test_analysis = get_analysis(test_patterns)
assert score(test_analysis) == 405
test_reanalysis = get_reanalysis(test_patterns, test_analysis)
assert rescore(test_reanalysis) == 400

real_patterns = parse_input(INPUT_FILE)
real_analysis = get_analysis(real_patterns)
print(f'Day {DAY} part 1: {score(real_analysis)}')
real_reanalysis = get_reanalysis(real_patterns, real_analysis)
print(f'Day {DAY} part 2: {rescore(real_reanalysis)}')
