from day20 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  assert Maze(TEST_INPUT_FILE).count_cheats(10) == 10
  assert Maze(TEST_INPUT_FILE).cheat_counts2[50] == 32
  assert Maze(TEST_INPUT_FILE).cheat_counts2[52] == 31
  assert Maze(TEST_INPUT_FILE).cheat_counts2[54] == 29
  assert Maze(TEST_INPUT_FILE).cheat_counts2[56] == 39
  assert Maze(TEST_INPUT_FILE).cheat_counts2[58] == 25
  assert Maze(TEST_INPUT_FILE).cheat_counts2[60] == 23
  assert Maze(TEST_INPUT_FILE).cheat_counts2[62] == 20
  assert Maze(TEST_INPUT_FILE).cheat_counts2[64] == 19
  assert Maze(TEST_INPUT_FILE).cheat_counts2[66] == 12
  assert Maze(TEST_INPUT_FILE).cheat_counts2[68] == 14
  assert Maze(TEST_INPUT_FILE).cheat_counts2[70] == 12
  assert Maze(TEST_INPUT_FILE).cheat_counts2[72] == 22
  assert Maze(TEST_INPUT_FILE).cheat_counts2[74] == 4
  assert Maze(TEST_INPUT_FILE).cheat_counts2[76] == 3
  print('Tests pass.')

if __name__ == '__main__':
  main()
