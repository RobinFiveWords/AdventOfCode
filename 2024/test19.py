from day19 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert Analysis(TEST_INPUT_FILE).count_valid() == 6
  assert Analysis(TEST_INPUT_FILE).count_ways() == 16
  print('Tests pass.')

if __name__ == '__main__':
  main()
