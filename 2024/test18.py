from day18 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'

TEST_EXIT = Point(6, 6)

def main():
  assert Space(TEST_INPUT_FILE, TEST_EXIT).shortest(12) == 22
  assert Space(TEST_INPUT_FILE, TEST_EXIT).search(12) == '6,1'
  print('Tests pass.')

if __name__ == '__main__':
  main()
