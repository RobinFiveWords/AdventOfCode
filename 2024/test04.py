from day04 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

def main():
  assert count1(parse_input(TEST_INPUT_FILE)) == 18
  assert count2(parse_input(TEST_INPUT_FILE)) == 9
  print('Tests pass.')

if __name__ == '__main__':
  main()
