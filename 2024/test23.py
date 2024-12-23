from day23 import *

DAY = int(__file__.split('/')[-1][4:6])
TEST_INPUT_FILE = f'testinput{DAY:02d}.txt'



def main():
  network = Network(TEST_INPUT_FILE)
  assert network.t3s() == 7
  assert network.password() == 'co,de,ka,ta'
  print('Tests pass.')

if __name__ == '__main__':
  main()
