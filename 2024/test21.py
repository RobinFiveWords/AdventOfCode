from day21 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert sum(map(complexity, parse_input(TEST_INPUT_FILE))) == 126384
  assert sum(map(lambda code: complexity2(code, 2), parse_input(TEST_INPUT_FILE))) == 126384
  assert sum(map(complexity, parse_input(INPUT_FILE))) == \
      sum(map(lambda code: complexity2(code, 2), parse_input(INPUT_FILE)))
  print('Tests pass.')

if __name__ == '__main__':
  main()
