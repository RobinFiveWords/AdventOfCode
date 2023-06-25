import java.util.HashMap;
import java.util.HashSet;
import java.util.Set;

// worked through lots of issues with an inner class
// and how to use it as keys in set/map (override equals and hashCode)
// a good hashCode function, one that avoids collisions,
// really seems to make a difference as it avoids falling back on equals
// (a lot more to learn about hash functions, I'm sure)

// created class as container for returning multiple values

// still not comfortable with static (class) variables;
// it seems they can be declared in the outer class body
// but assignments must be within a static block

// learned to use -ea command line flag to enable assertions
// bailed on explicitly copying a set
// and on taking the min of a collection

class Day12 {

  private static class Pt {
    private int x;
    private int y;

    public Pt(int x, int y) {
      this.x = x;
      this.y = y;
    }

    @Override
    public boolean equals(Object other) {
      Pt otherPt = (Pt)other;
      return this.x == otherPt.x && this.y == otherPt.y;
    }

    @Override
    public int hashCode() {
      return this.x ^ (this.y << 16);
    }

    public Pt add(Pt other) {
      return new Pt(this.x + other.x, this.y + other.y); 
    }

    public int x() { return this.x; }
    public int y() { return this.y; }

    public String toString() {
      return "Pt(" + x() + ", " + y() + ")";
    }
  }

  private static class Parsed {
    private HashMap<Pt, Integer> heights;
    private Pt start;
    private Pt goal;

    public Parsed(HashMap<Pt, Integer> heights, Pt start, Pt goal) {
      this.heights = heights;
      this.start = start;
      this.goal = goal;
    }

    public HashMap<Pt, Integer> heights() { return heights; }
    public Pt start() { return start; }
    public Pt goal() { return goal; }
  }

  private static void assertOccurrences(String[] ss, char c, int n) {
    int count = 0;
    for (String s : ss) {
      count += s.chars().filter(ch -> ch == c).count();
    }
    assert count == n;
  }

  private static Pt[] directions;
  static {
    directions = new Pt[4];
    directions[0] = new Pt( 0, -1);  // Up
    directions[1] = new Pt( 0,  1);  // Down
    directions[2] = new Pt(-1,  0);  // Left
    directions[3] = new Pt( 1,  0);  // Right
  }

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile("2022day12testinput.txt");
    assertOccurrences(testData, 'S', 1);
    assertOccurrences(testData, 'E', 1);

    String[] realData = aocUtils.bufferLinesFromFile("2022day12input.txt");
    assertOccurrences(realData, 'S', 1);
    assertOccurrences(realData, 'E', 1);

    Parsed testParsed = parseInput(testData);
    HashMap<Pt, Integer> testHeights = testParsed.heights();
    Pt testStart = testParsed.start();
    Pt testGoal = testParsed.goal();
    assert search1(testHeights, testStart, testGoal) == 31;
    assert search2(testHeights, testGoal) == 29;

    Parsed realParsed = parseInput(realData);
    HashMap<Pt, Integer> realHeights = realParsed.heights();
    Pt realStart = realParsed.start();
    Pt realGoal = realParsed.goal();
    int part1 = search1(realHeights, realStart, realGoal);
    System.out.println("Day 12 part 1: " + part1);
    int part2 = search2(realHeights, realGoal);
    System.out.println("Day 12 part 2: " + part2);
  }

  private static Parsed parseInput(String[] data) {
    HashMap<Pt, Integer> heights = new HashMap<Pt, Integer>();
    Pt start = new Pt(Integer.MIN_VALUE, Integer.MIN_VALUE);
    Pt goal = new Pt(Integer.MIN_VALUE, Integer.MIN_VALUE);

    for (int y = 0; y < data.length; y++) {
      for (int x = 0; x < data[y].length(); x++) {
        char c = data[y].charAt(x);
        if (c == 'S') {
          start = new Pt(x, y);
          heights.put(start, Character.getNumericValue('a'));
        } else if (c == 'E') {
          goal = new Pt(x, y);
          heights.put(goal, Character.getNumericValue('z'));
        } else {
          heights.put(new Pt(x, y), Character.getNumericValue(c));
        }
      }
    }
    return new Parsed(heights, start, goal);
  }

  private static int search1(HashMap<Pt, Integer> heights,
                             Pt start,
                             Pt goal) {
    Set<Pt> visited = new HashSet<Pt>();
    visited.add(start);
    int steps = 0;
    Set<Pt> alive = new HashSet<Pt>();
    alive.add(start);
    Set<Pt> stillAlive = new HashSet<Pt>();
    for (;;) {
      if (alive.size() == 0) {
        return Integer.MAX_VALUE;
      }
      for (Pt currentPt : alive) {
        for (Pt direction : Day12.directions) {
          Pt neighborPt = currentPt.add(direction);
          Integer height = heights.get(neighborPt);
          if (!visited.contains(neighborPt) && height != null) {
            if (height <= heights.get(currentPt) + 1) {
              visited.add(neighborPt);
              stillAlive.add(neighborPt);
              if (neighborPt.equals(goal)) {
                return steps + 1;
              }
            }
          }
        }
      }
      alive.clear();
      for (Pt alivePt : stillAlive) {
        alive.add(alivePt);
      }
      stillAlive.clear();
      steps++;
    }
  }

  private static int search2(HashMap<Pt, Integer> heights,
                             Pt goal) {
    int lowestHeight = Character.getNumericValue('a');
    int best = Integer.MAX_VALUE;
    for (Pt start : heights.keySet()) {
      if (heights.get(start) == lowestHeight) {
        int result = search1(heights, start, goal);
        if (result < best) best = result;
      }
    }
    return best;
  }
}