from day13 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  machines = parse_input(TEST_INPUT_FILE)
  assert total_cost(machines) == 480
  assert cost(machines[0], BIG_N) == 0
  assert cost(machines[1], BIG_N) > 0
  assert cost(machines[2], BIG_N) == 0
  assert cost(machines[3], BIG_N) > 0
  print('Tests pass.')

if __name__ == '__main__':
  main()
