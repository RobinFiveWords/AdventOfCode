from day10 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert Map(TEST_INPUT_FILE).total_score() == 36
  assert Map(TEST_INPUT_FILE).total_score2() == 81
  print('Tests pass.')

if __name__ == '__main__':
  main()
