from day11 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

TEST1 = '0 1 10 99 999'
TEST2 = '125 17'

def main():
  test_stones = [parse_ints(TEST2)]
  append(test_stones, 25)
  assert len(test_stones[-1]) == 55312
  print('Tests pass.')

if __name__ == '__main__':
  main()
