import java.lang.Math;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

class Day09 {
  static String TEST_INPUT_FILE = "2022day09testinput.txt";
  static String TEST_INPUT_FILE2 = "2022day09testinput2.txt";
  static String INPUT_FILE = "2022day09input.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    List<ParsedOne> testInstructions = parseInput(testData);
    assert uniqueTailPositions(testInstructions, 1) == 13;
    assert uniqueTailPositions(testInstructions, 9) == 1;

    String[] testData2 = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE2);
    List<ParsedOne> testInstructions2 = parseInput(testData2);
    assert uniqueTailPositions(testInstructions2, 9) == 36;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    List<ParsedOne> realInstructions = parseInput(realData);

    int part1 = uniqueTailPositions(realInstructions, 1);
    System.out.println("Day 9 part 1: " + part1);

    int part2 = uniqueTailPositions(realInstructions, 9);
    System.out.println("Day 9 part 2: " + part2);
  }

  private static int uniqueTailPositions(List<ParsedOne> instructions,
                                         int numRopes) {
    Set<Pt> positions = new HashSet<>();
    List<Pt> moves = new ArrayList<>();

    // initial moves
    for (ParsedOne instruction : instructions) {
      Pt direction = instruction.direction;
      int steps = instruction.steps;
      for (int i = 0; i < steps; i++) {
        moves.add(direction);
      }
    }

    for (int i = 0; i < numRopes; i++) {
      Rope rope = moveRope(moves);
      moves = rope.getMoves();
      positions = rope.getTailPositions();
    }

    return positions.size();
  }

  private static Rope moveRope(List<Pt> moves) {
    Rope rope = new Rope();
    for (Pt move : moves) {
      rope.moveHead(move);
    }
    return rope;
  }

  private static class Rope {
    private Pt head;
    private Pt tail;
    private Set<Pt> tailPositions;
    private List<Pt> moves;

    Rope() {
      this.head = new Pt(0, 0);
      this.tail = new Pt(0, 0);
      this.tailPositions = new HashSet<>();
      this.tailPositions.add(new Pt(0, 0));
      this.moves = new ArrayList<>();
    }

    public void moveHead(Pt deltaPt) {
      this.head = this.head.add(deltaPt);
      int xdiff = this.head.x() - this.tail.x();
      int ydiff = this.head.y() - this.tail.y();
      if (Math.abs(xdiff) == 2 || Math.abs(ydiff) == 2) {
        Pt moveTail = new Pt(Integer.signum(xdiff), Integer.signum(ydiff));
        this.tail = this.tail.add(moveTail);
        this.tailPositions.add(this.tail);
        this.moves.add(moveTail);
      }
    }

    public Pt head() { return this.head; }
    public Pt tail() { return this.tail; }
    public List<Pt> getMoves() { return this.moves; }
    public Set<Pt> getTailPositions() { return this.tailPositions; }

    public String toString() {
      return "Rope(head=(" + this.head.x() + "," + this.head.y() +
               "), tail=(" + this.tail.x() + "," + this.tail.y() + ")";
    }
  }

  private static class ParsedOne {
    private Pt direction;
    private int steps;

    ParsedOne(String s) {
      String[] row = s.split(" ");
      switch(row[0]) {
        case "U":
          this.direction = new Pt( 0,  1);
          break;
        case "D":
          this.direction = new Pt( 0, -1);
          break;
        case "L":
          this.direction = new Pt(-1,  0);
          break;
        case "R":
          this.direction = new Pt( 1,  0);
          break;
      }
      this.steps = Integer.parseInt(row[1]);
    }
  }

  private static List<ParsedOne> parseInput(String[] data) {
    List<ParsedOne> results = new ArrayList<>();
    for (String s : data) {
      results.add(new ParsedOne(s));
    }
    return results;
  }
}