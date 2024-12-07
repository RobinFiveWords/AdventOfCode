from day07 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

def main():
  assert concatenate(12, 345) == 12345

  assert sum(map(lambda ints: possible(ints, OPERATORS), parse_input(TEST_INPUT_FILE))) == 3749
  assert sum(map(lambda ints: possible(ints, OPERATORS2), parse_input(TEST_INPUT_FILE))) == 11387
  print('Tests pass.')

if __name__ == '__main__':
  main()
