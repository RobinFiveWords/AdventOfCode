import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

class Day11 {
  static String TEST_INPUT_FILE = "2022day11testinput.txt";
  static String INPUT_FILE = "2022day11input.txt";

  public static void main(String[] args) throws Exception {
    String testNotes = aocUtils.readFileAsString(TEST_INPUT_FILE);
    List<Monkey> testMonkeys1 = simulate(testNotes, 20, true);
    // for (Monkey monkey : testMonkeys1) {
    //   System.out.println(monkey);
    // }
    long testMB1 = monkeyBusiness(testMonkeys1);
    assert testMB1 == 10605L;
    List<Monkey> testMonkeys2 = simulate(testNotes, 10000, false);
    long testMB2 = monkeyBusiness(testMonkeys2);
    assert testMB2 == 2713310158L;

    String realNotes = aocUtils.readFileAsString(INPUT_FILE);
    List<Monkey> realMonkeys1 = simulate(realNotes, 20, true);
    System.out.println("Day 11 part 1: " + monkeyBusiness(realMonkeys1));
    List<Monkey> realMonkeys2 = simulate(realNotes, 10000, false);
    System.out.println("Day 11 part 2: " + monkeyBusiness(realMonkeys2));
  }

  private static List<Monkey> simulate(String notes,
                                       int rounds,
                                       boolean relief) {
    List<Monkey> monkeys = new ArrayList<Monkey>();
    for (String details : notes.split("\n\n")) {
      monkeys.add(new Monkey(details));
    }

    int[] divisors = new int[monkeys.size()];
    for (int i = 0; i < divisors.length; i++) {
      divisors[i] = monkeys.get(i).divisibleBy();
    }
    int modulus = aocUtils.lcm(divisors);

    for (int round = 0; round < rounds; round++) {
      for (Monkey monkey : monkeys) {
        monkey.turn(relief);
        for (long n : monkey.sendToTrue) {
          monkeys.get(monkey.idxIfTrue).items.enqueue(n % modulus);
        }
        for (long n : monkey.sendToFalse) {
          monkeys.get(monkey.idxIfFalse).items.enqueue(n % modulus);
        }
        monkey.sendToTrue.clear();
        monkey.sendToFalse.clear();
      }
    }
    return monkeys;
  }

  private static long monkeyBusiness(List<Monkey> monkeys) {
    Long[] inspected = new Long[monkeys.size()];
    for (int i = 0; i < inspected.length; i++) {
      inspected[i] = monkeys.get(i).totalInspected();
    }
    Arrays.sort(inspected, Collections.reverseOrder());
    return inspected[0] * inspected[1];
  }

  private static class Monkey {
    private String details;
    public Queue<Long> items;
    private long totalInspected;
    private String op;
    private String val;
    private int divisibleBy;
    private int idxIfTrue;
    private int idxIfFalse;
    public List<Long> sendToTrue;
    public List<Long> sendToFalse;

    public Monkey(String details) {
      String[] rows = details.split("\n");

      this.items = new Queue<Long>();
      String[] startingItems = rows[1].trim().split(" ");
      for (int i = 2; i < startingItems.length; i++) {
        items.enqueue(Long.parseLong(startingItems[i].replace(",", "")));
      }

      this.totalInspected = 0L;
      this.op  = rows[2].trim().split(" ")[4];
      this.val = rows[2].trim().split(" ")[5];
      this.divisibleBy = Integer.parseInt(rows[3].trim().split(" ")[3]);
      this.idxIfTrue   = Integer.parseInt(rows[4].trim().split(" ")[5]);
      this.idxIfFalse  = Integer.parseInt(rows[5].trim().split(" ")[5]);
      this.sendToTrue  = new ArrayList<Long>();
      this.sendToFalse = new ArrayList<Long>();
    }

    public void turn(boolean relief) {
      while (!items.isEmpty()) {
        long oldVal = items.dequeue();
        long newVal;
        if (val.equals("old")) {
          newVal = oldVal * oldVal;
        } else if (op.equals("*")) {
          newVal = oldVal * Long.parseLong(val);
        } else {  // (op.equals("+"))
          newVal = oldVal + Long.parseLong(val);
        }
        totalInspected++;
        if (relief) newVal /= 3;
        if (newVal % divisibleBy == 0) {
          sendToTrue.add(newVal);
        } else {
          sendToFalse.add(newVal);
        }
      }
    }

    public long totalInspected() { return totalInspected; }
    public int divisibleBy() { return divisibleBy; }

    public String toString() {
      String result = "";
      int lengthQueue = items.size();
      for (int i = 0; i < lengthQueue; i++) {
        long n = items.dequeue();
        if (i == 0) {
          result += n;
        } else {
          result += ", " + n;
        }
        items.enqueue(n);
      }
      return result;
    }
  }
}