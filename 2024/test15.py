from day15 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'
TEST_INPUT_FILE2 = f'testinput{DAY:02d}.txt'.replace('.txt', 'b.txt')
TEST_INPUT_FILE3 = f'testinput{DAY:02d}.txt'.replace('.txt', 'c.txt')



def main():
  assert Warehouse(TEST_INPUT_FILE).execute() == 2028
  assert Warehouse(TEST_INPUT_FILE2).execute() == 10092
  assert Warehouse2(TEST_INPUT_FILE2).execute() == 9021
  print('Tests pass.')

if __name__ == '__main__':
  main()
