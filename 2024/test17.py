from day17 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert Computer(TEST_INPUT_FILE).run() == '4,6,3,5,6,3,5,2,1,0'
  print('Tests pass.')

if __name__ == '__main__':
  main()
