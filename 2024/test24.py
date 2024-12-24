from day24 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'
TEST_INPUT_FILE2 = f'testinput{DAY:02d}b.txt'
INPUT_FILE_ADJUSTED = f'input{DAY:02d}adjusted.txt'



def main():
  assert Wires(TEST_INPUT_FILE).evaluate() == 4
  assert Wires(TEST_INPUT_FILE2).evaluate() == 2024
  a = Wires(INPUT_FILE_ADJUSTED)
  assert a.number('x') + a.number('y') == a.evaluate()
  print('Tests pass.')

if __name__ == '__main__':
  main()
