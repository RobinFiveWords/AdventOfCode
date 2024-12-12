from day12 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'
TEST_INPUT_FILE1 = f'testinput{DAY:02d}.txt'.replace('.txt', 'a.txt')
TEST_INPUT_FILE2 = f'testinput{DAY:02d}.txt'.replace('.txt', 'b.txt')
TEST_INPUT_FILE3 = f'testinput{DAY:02d}.txt'.replace('.txt', 'c.txt')
TEST_INPUT_FILE4 = f'testinput{DAY:02d}.txt'.replace('.txt', 'd.txt')



def main():
  assert Garden(TEST_INPUT_FILE).total_price() == 140
  assert Garden(TEST_INPUT_FILE1).total_price() == 772
  assert Garden(TEST_INPUT_FILE2).total_price() == 1930
  assert Garden(TEST_INPUT_FILE).total_price2() == 80
  assert Garden(TEST_INPUT_FILE1).total_price2() == 436
  assert Garden(TEST_INPUT_FILE2).total_price2() == 1206
  assert Garden(TEST_INPUT_FILE3).total_price2() == 236
  assert Garden(TEST_INPUT_FILE4).total_price2() == 368
  print('Tests pass.')

if __name__ == '__main__':
  main()
