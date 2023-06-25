import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;



public class Day17 {
  static String ROCKS_FILE = "2022day17rocks.txt";
  static String INPUT_FILE = "2022day17input.txt";

  static int ROWS_FOR_BITMASK = 9;

  static long bigN = 1000000000000L;

  static String testData = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>";

  static Map<Character, Integer> jetEncodings = new HashMap<Character, Integer>();
  static {
    jetEncodings.put('<', -1);
    jetEncodings.put('>',  1);
  }

  static Pt down  = new Pt( 0, -1);
  static Pt left  = new Pt(-1,  0);
  static Pt right = new Pt( 1,  0);

  private static List<Set<Pt>> generateRocks(String rocksFile) throws Exception {
    List<Set<Pt>> rocks = new ArrayList<Set<Pt>>();
    String rockData = aocUtils.readFileAsString(rocksFile);
    String[] rockStrings = rockData.split("\n\n");

    for (String rockString : rockStrings) {
      String[] rockRows = rockString.split("\n");
      Set<Pt> newRock = new HashSet<Pt>();
      for (int y = 0; y < rockRows.length; y++) {
        for (int x = 0; x < rockRows[y].length(); x++) {
          if (rockRows[rockRows.length - 1 - y].charAt(x) == '#') {
            newRock.add(new Pt(x, y));
          }
        }
      }
      rocks.add(newRock);
    }

    return rocks;
  }

  public static void main(String[] args) throws Exception {
    String realData = aocUtils.readFileAsString(INPUT_FILE);
    List<Set<Pt>> rocks = generateRocks(ROCKS_FILE);

    Cave testCave = new Cave(testData, rocks);
    testCave.run();
    assert testCave.heights.get(2022) == 3068;
    assert testCave.bigNheight == 1514285714288L;

    Cave realCave = new Cave(realData, rocks);
    realCave.run();
    System.out.println("Day 17 part 1: " + realCave.heights.get(2022));
    System.out.println("Day 17 part 2: " + realCave.bigNheight);
  }

  private static class Cave {
    private boolean running;
    private boolean cycling;

    // these all start at zero
    private int nextJetIndex;
    private int nextRockIndex;
    private int ymax;
    private int totalRocks;

    private int jetLength;
    private int rockLength;

    private int[] jets;
    private List<Set<Pt>> rocks;

    private Set<Pt> landedRocks;
    private List<Integer> heights;
    private Set<State> firstPass;
    private Map<State, Integer> secondPass;

    private long bigNheight;

    Cave(String jetData, List<Set<Pt>> rocks) {
      this.landedRocks = new HashSet<Pt>();
      this.heights = new ArrayList<Integer>();
      heights.add(0);
      this.firstPass = new HashSet<State>();
      this.secondPass = new HashMap<State, Integer>();

      this.jetLength = jetData.length();
      this.jets = new int[this.jetLength];
      for (int i = 0; i < this.jetLength; i++) {
        this.jets[i] = jetEncodings.get(jetData.charAt(i));
      }

      this.rocks = rocks;
      this.rockLength = rocks.size();

      this.running = true;
      this.cycling = true;
    }

    void absorbRock(Rock rock) {
      int tmpY;
      for (Pt coord : rock.coords) {
        this.landedRocks.add(coord);
        if ((tmpY = coord.y()) > this.ymax) this.ymax = tmpY;
      }
      this.totalRocks++;
      this.heights.add(this.ymax);
    }

    void advanceJet() {
      this.nextJetIndex++;
      if (this.nextJetIndex == this.jetLength) this.nextJetIndex = 0;
    }

    void advanceRock() {
      this.nextRockIndex++;
      if (this.nextRockIndex == this.rockLength) this.nextRockIndex = 0;
    }

    State createState() {
      StringBuilder bitmask = new StringBuilder();
      for (int i = 0; i < ROWS_FOR_BITMASK; i++) {
        int y = ymax - i;
        for (int x = 0; x < 7; x++) {
          if (landedRocks.contains(new Pt(x, y))) {
            bitmask.append("1");
          } else {
            bitmask.append("0");
          }
        }
      }
      return new State(bitmask.toString(), nextJetIndex, nextRockIndex);
    }

    void run() {
      while (running) {
        Rock currentRock = new Rock(rocks.get(nextRockIndex), ymax);
        while (currentRock.falling) {
          if (jets[nextJetIndex] == -1) {
            currentRock.checkMove(left, this);
          } else {
            currentRock.checkMove(right, this);
          }
          advanceJet();
          currentRock.checkMove(down, this);
        }
        absorbRock(currentRock);
        advanceRock();

        if (cycling) {
          State state = createState();
          if (firstPass.contains(state)) {
            if (secondPass.containsKey(state)) {
              int prevRocks = secondPass.get(state);
              int cycleLength = totalRocks - prevRocks;
              int cycleHeight = heights.get(totalRocks) - heights.get(prevRocks);
              long rocksToGo = bigN - totalRocks;
              long cyclesToGo = rocksToGo / cycleLength;
              int remainder = (int)(rocksToGo % cycleLength);
              int backUp = 0;
              if (remainder > 0) {
                cyclesToGo++;
                backUp = cycleLength - remainder;
              }
              bigNheight = (heights.get(totalRocks - backUp)
                            + cyclesToGo * cycleHeight);
              cycling = false;
            } else {
              secondPass.put(state, totalRocks);
            }
          } else {
            firstPass.add(state);
          }
        }

        if (heights.size() > 2022 && !cycling) running = false;
      }
    }
  }

  private static class Rock {
    private Set<Pt> coords;
    private boolean falling;

    Rock(Set<Pt> coords, int caveYmax) {
      Pt offset = new Pt(2, caveYmax + 4);
      this.coords = new HashSet<Pt>();
      for (Pt coord : coords) {
        this.coords.add(coord.add(offset));
      }
      this.falling = true;
    }

    boolean checkMove(Pt direction, Cave cave) {
      Set<Pt> newCoords = new HashSet<Pt>();
      for (Pt coord : this.coords) {
        newCoords.add(coord.add(direction));
      }

      if (direction.equals(left)) {
        for (Pt coord : newCoords) {
          if (coord.x() == -1) return false;
        }
      } else if (direction.equals(right)) {
        for (Pt coord : newCoords) {
          if (coord.x() == 7) return false;
        }        
      } else { // down
        for (Pt coord : newCoords) {
          if (coord.y() == 0) {
            this.falling = false;
            return false;
          }
        }
      }

      for (Pt coord : newCoords) {
        if (cave.landedRocks.contains(coord)) {
          if (direction.equals(down)) this.falling = false;
          return false;
        }
      }

      // won't overlap with cave rocks
      this.coords.clear();
      for (Pt coord : newCoords) {
        this.coords.add(coord);
      }
      return true;
    }

    void move(Pt direction) {
      // can use when there's no possibility of collision
      Set<Pt> newCoords = new HashSet<Pt>();
      for (Pt coord : this.coords) {
        newCoords.add(coord.add(direction));
      }
      this.coords.clear();
      for (Pt coord : newCoords) {
        this.coords.add(coord);
      }
    }

    public String toString() { return coords.toString(); }
  }

  private static class State {
    private long topRockBits;
    private int nextJetIndex;
    private int nextRockIndex;

    State(long topRockBits, int nextJetIndex, int nextRockIndex) {
      this.topRockBits = topRockBits;
      this.nextJetIndex = nextJetIndex;
      this.nextRockIndex = nextRockIndex;
    }

    State(String topRockString, int nextJetIndex, int nextRockIndex) {
      this.topRockBits = Long.parseLong(topRockString, 2);
      this.nextJetIndex = nextJetIndex;
      this.nextRockIndex = nextRockIndex;
    }

    @Override
    public boolean equals(Object other) {
      State otherState = (State)other;
      return (this.topRockBits == otherState.topRockBits
              && this.nextJetIndex == otherState.nextJetIndex
              && this.nextRockIndex == otherState.nextRockIndex);
    }

    @Override
    public int hashCode() {
      return (int)(Long.hashCode(this.topRockBits)
                   + Integer.hashCode(this.nextJetIndex)
                   + Integer.hashCode(this.nextRockIndex));
    }

    public String toString() {
      return ("State("
              + topRockBits + ", "
              + nextJetIndex + ", "
              + nextRockIndex + ")"
              );
    }
  }
}