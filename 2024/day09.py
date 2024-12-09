

DAY = int(__file__.split('/')[-1][3:5])
INPUT_FILE = f'input{DAY:02d}.txt'

def parse_file(file):
  with open(file) as f:
    return f.read().strip()

def parse_string(s):
  memory = {}
  position = 0
  fid = 0
  for i, char in enumerate(s):
    n = int(char)
    if i % 2 == 0:  # file
      for _ in range(n):
        memory[position] = fid
        position += 1
    else:  # free space
      position += n
      fid += 1
  return memory

def defragment(memory):
  last = max(memory)
  empty = 0
  if 0 in memory:
    empty = min(memory)
    while empty in memory:
      empty += 1
  while empty < last:
    memory[empty] = memory[last]
    del memory[last]
    while empty in memory:
      empty += 1
    while last not in memory:
      last -= 1
  return memory

def display(memory):
  output = []
  for i in range(len(memory)):
    output.append(memory.get(i, '.'))
  return ''.join(str(x) for x in output)

def checksum(memory):
  return sum(k * v for k, v in memory.items())

def parse_string2(s):
  files = []
  gaps = []
  position = 0
  for i, char in enumerate(s):
    n = int(char)
    if i % 2 == 0:  # file
      files.append((position, n))
    else:
      gaps.append((position, n))
    position += n
  return files, gaps

def defragment2(files, gaps):
  files = files.copy()
  gaps = gaps.copy()
  for file_index in range(len(files) - 1, -1, -1):
    file_position, file_length = files[file_index]
    for gap_index, (gap_position, gap_length) in enumerate(gaps):
      if file_position - file_length < gap_position:
        break
      if file_length > gap_length:
        continue
      files[file_index] = (gap_position, file_length)
      if gap_length == file_length:
        del gaps[gap_index]
      else:
        gaps[gap_index] = (gap_position + file_length, gap_length - file_length)
      break
  return files, gaps

def checksum2(files):
  return sum(fid * (position + i)
             for fid, (position, length) in enumerate(files)
             for i in range(length))

def main():
  memory = parse_string(parse_file(INPUT_FILE))
  print(f'Day {DAY} part 1: {checksum(defragment(memory))}')

  files2, gaps2 = parse_string2(parse_file(INPUT_FILE))
  defiles2, degaps2 = defragment2(files2, gaps2)
  print(f'Day {DAY} part 2: {checksum2(defiles2)}')
  pass

if __name__ == '__main__':
  main()
