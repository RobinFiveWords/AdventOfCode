from day25 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert count_fits(*parse_input(TEST_INPUT_FILE)) == 3
  print('Tests pass.')

if __name__ == '__main__':
  main()
