import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Day23 {
  static String INPUT_FILE = "2022day23input.txt";
  static String TEST_INPUT_FILE = "2022day23testinput.txt";
  // static String TEST_INPUT_FILE = "2022day23smalltestinput.txt";

  static Pt N  = new Pt( 0, -1);
  static Pt NE = new Pt( 1, -1);
  static Pt E  = new Pt( 1,  0);
  static Pt SE = new Pt( 1,  1);
  static Pt S  = new Pt( 0,  1);
  static Pt SW = new Pt(-1,  1);
  static Pt W  = new Pt(-1,  0);
  static Pt NW = new Pt(-1, -1);

  static Set<Pt> allDirections = new HashSet<Pt>();
  static {
    allDirections.add(N);
    allDirections.add(NE);
    allDirections.add(E);
    allDirections.add(SE);
    allDirections.add(S);
    allDirections.add(SW);
    allDirections.add(W);
    allDirections.add(NW);
  }

  private static List<List<Pt>> generateStartingRules() {
    List<List<Pt>> rules = new ArrayList<List<Pt>>();
    List<Pt> ruleN = new ArrayList<Pt>();
    List<Pt> ruleS = new ArrayList<Pt>();
    List<Pt> ruleE = new ArrayList<Pt>();
    List<Pt> ruleW = new ArrayList<Pt>();

    ruleN.add(N);
    ruleN.add(NE);
    ruleN.add(NW);

    ruleS.add(S);
    ruleS.add(SE);
    ruleS.add(SW);

    ruleW.add(W);
    ruleW.add(NW);
    ruleW.add(SW);

    ruleE.add(E);
    ruleE.add(NE);
    ruleE.add(SE);

    rules.add(ruleN);
    rules.add(ruleS);
    rules.add(ruleW);
    rules.add(ruleE);

    return rules;
  }

  public static void main(String[] args) throws Exception {
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Set<Pt> testElves = parseRows(testRows);
    List<List<Pt>> testRules = generateStartingRules();
    boolean testRunning = true;
    int testRounds = 0;
    int test1 = 0;
    while (testRunning) {
      testRounds++;
      testRunning = round(testElves, testRules);
      if (testRounds == 10) test1 = tiles(testElves);
    }
    assert test1 == 110;
    assert testRounds == 20;
    // printElves(testElves);

    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Set<Pt> realElves = parseRows(realRows);
    List<List<Pt>> realRules = generateStartingRules();
    boolean realRunning = true;
    int realRounds = 0;
    while (realRunning) {
      realRounds++;
      realRunning = round(realElves, realRules);
      if (realRounds == 10) System.out.println("Day 23 part 1: " + tiles(realElves));
    }
    System.out.println("Day 23 part 2: " + realRounds);
    // printElves(realElves);
  }

  private static Set<Pt> parseRows(String[] rows) {
    Set<Pt> results = new HashSet<Pt>();
    for (int y = 0; y < rows.length; y++) {
      for (int x = 0; x < rows[y].length(); x++) {
        if (rows[y].charAt(x) == '#') results.add(new Pt(x, y));
      }
    }
    return results;
  }

  private static boolean round(Set<Pt> elves, List<List<Pt>> rules) {
    Map<Pt, Pt> proposedMoves = proposeMoves(elves, rules);
    if (proposedMoves.isEmpty()) return false;
    resolveMoves(elves, proposedMoves);
    Collections.rotate(rules, -1);
    return true;
  }

  private static void resolveMoves(Set<Pt> elves, Map<Pt, Pt> proposedMoves) {
    Set<Pt> first = new HashSet<Pt>();
    Set<Pt> duplicates = new HashSet<Pt>();
    for (Map.Entry<Pt, Pt> kv : proposedMoves.entrySet()) {
      Pt destination = kv.getValue();
      if (first.contains(destination)) {
        duplicates.add(destination);
      } else {
        first.add(destination);
      }
    }
    first.removeAll(duplicates);

    Pt newElf;
    for (Map.Entry<Pt, Pt> kv : proposedMoves.entrySet()) {
      if (first.contains((newElf = kv.getValue()))) {
        elves.add(newElf);
        elves.remove(kv.getKey());
      }
    }
  }

  private static Map<Pt, Pt> proposeMoves(Set<Pt> elves, List<List<Pt>> rules) {
    Map<Pt, Pt> results = new HashMap<Pt, Pt>();
    for (Pt elf : elves) {
      Pt proposedMove = proposeMove(elf, elves, rules);
      if (proposedMove == null) continue;
      results.put(elf, proposedMove);
    }
    return results;
  }

  private static Pt proposeMove(Pt elf, Set<Pt> elves, List<List<Pt>> rules) {
    boolean isolated = true;
    for (Pt direction : allDirections) {
      if (elves.contains(elf.add(direction))) {
        isolated = false;
        break;
      }
    }
    if (isolated) return null;
    for (List<Pt> rule : rules) {
      boolean followRule = true;
      for (Pt direction : rule) {
        if (elves.contains(elf.add(direction))) {
          followRule = false;
          break;
        }
      }
      if (followRule) return elf.add(rule.get(0));
    }
    return null;
  }

  private static int tiles(Set<Pt> elves) {
    int minX = Integer.MAX_VALUE;
    int maxX = Integer.MIN_VALUE;
    int minY = Integer.MAX_VALUE;
    int maxY = Integer.MIN_VALUE;
    int x, y;
    for (Pt elf : elves) {
      if ((x = elf.x()) < minX) minX = x;
      if ((x = elf.x()) > maxX) maxX = x;
      if ((y = elf.y()) < minY) minY = y;
      if ((y = elf.y()) > maxY) maxY = y;
    }
    return (maxX - minX + 1) * (maxY - minY + 1) - elves.size();
  }

  private static void printElves(Set<Pt> elves) {
    int minX = Integer.MAX_VALUE;
    int maxX = Integer.MIN_VALUE;
    int minY = Integer.MAX_VALUE;
    int maxY = Integer.MIN_VALUE;
    int x, y;
    for (Pt elf : elves) {
      if ((x = elf.x()) < minX) minX = x;
      if ((x = elf.x()) > maxX) maxX = x;
      if ((y = elf.y()) < minY) minY = y;
      if ((y = elf.y()) > maxY) maxY = y;
    }
    for (y = minY; y <= maxY; y++) {
      for (x = minX; x <= maxX; x++) {
        if (elves.contains(new Pt(x, y))) {
          System.out.print('#');
        } else {
          System.out.print('.');
        }
      }
      System.out.println();
    }    
  }
}