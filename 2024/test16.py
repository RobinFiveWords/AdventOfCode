from day16 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'
TEST_INPUT_FILE2 = f'testinput{DAY:02d}.txt'.replace('.txt', 'b.txt')



def main():
  assert Maze(TEST_INPUT_FILE).search() == 7036
  assert Maze(TEST_INPUT_FILE2).search() == 11048
  assert Maze(TEST_INPUT_FILE).search2() == 45
  assert Maze(TEST_INPUT_FILE2).search2() == 64
  print('Tests pass.')

if __name__ == '__main__':
  main()
