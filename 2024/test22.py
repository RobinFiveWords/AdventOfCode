from day22 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'
TEST_INPUT_FILE2 = f'testinput{DAY:02d}b.txt'



def main():
  assert sum(evolve_file(TEST_INPUT_FILE, 2000)) == 37327623
  assert max(Market(TEST_INPUT_FILE2).bests.values()) == 23
  print('Tests pass.')

if __name__ == '__main__':
  main()
