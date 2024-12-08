from day08 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

def main():
  assert Map(TEST_INPUT_FILE).within_bounds() == 14
  assert Map(TEST_INPUT_FILE).within_bounds2() == 34
  print('Tests pass.')

if __name__ == '__main__':
  main()
