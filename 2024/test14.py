from day14 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

XMOD = 11
YMOD = 7

def main():
  assert observe(parse_input(TEST_INPUT_FILE), 100, XMOD, YMOD) == 12
  print('Tests pass.')

if __name__ == '__main__':
  main()
