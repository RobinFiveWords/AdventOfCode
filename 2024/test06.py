from day06 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  test_lab = Lab(TEST_INPUT_FILE)
  assert test_lab.walk() == 41
  assert test_lab.search() == 6
  print('Tests pass.')

if __name__ == '__main__':
  main()
