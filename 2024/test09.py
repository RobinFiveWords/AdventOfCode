from day09 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

TEST1 = '12345'
TEST2 = '2333133121414131402'

def main():
  mem1 = parse_string(TEST1)
  mem2 = parse_string(TEST2)

  assert display(defragment(mem1)) == '022111222'
  assert display(defragment(mem2)) == '0099811188827773336446555566'
  assert checksum(defragment(mem2)) == 1928

  files2, gaps2 = parse_string2(TEST2)
  defiles2, degaps2 = defragment2(files2, gaps2)
  assert checksum2(defiles2) == 2858
  print('Tests pass.')

if __name__ == '__main__':
  main()
