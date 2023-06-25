import java.util.ArrayList;
import java.util.List;
import java.lang.Math;

class Day10 {
  static String TEST_INPUT_FILE = "2022day10testinput.txt";
  static String INPUT_FILE = "2022day10input.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    int[] testAdds = parseInput(testData);
    assert solve(testAdds) == 13140;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    int[] realAdds = parseInput(realData);
    System.out.println("Day 10 part 2:");
    int part1 = solve(realAdds);
    System.out.println("Day 10 part 1: " + part1);
  }

  private static int[] parseInput(String[] data) {
    List<Integer> adds = new ArrayList<Integer>();
    for (String instruction : data) {
      adds.add(0);
      String[] tokens = instruction.split(" ");
      if (tokens[0].equals("addx")) {
        adds.add(Integer.parseInt(tokens[1]));
      }
    }
    return adds.stream().mapToInt(i->i).toArray();
  }

  private static int solve(int[] adds) {
    int part1 = 0;
    int register = 1;
    int distance;
    for (int i = 1; i <= adds.length; i++) {
      // part 2
      distance = Math.abs(register - ((i-1) % 40));
      if (distance <= 1) {
        System.out.print("#");
      } else {
        System.out.print(".");
      }
      if (i % 40 == 0) {
        System.out.println();
      }

      // part 1
      register += adds[i-1];
      if (i > 0 && i % 40 == 19) {
        part1 += ( register * (i+1) );
      }
    }
    return part1;
  }
}