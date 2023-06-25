import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class Day24 {
  static String INPUT_FILE = "2022day24input.txt";
  static String TEST_INPUT_FILE = "2022day24testinput.txt";
  // static String TEST_INPUT_FILE = "2022day24smalltestinput.txt";

  static Pt RIGHT = new Pt( 1,  0);
  static Pt DOWN  = new Pt( 0,  1);
  static Pt LEFT  = new Pt(-1,  0);
  static Pt UP    = new Pt( 0, -1);
  static Pt STAY  = new Pt( 0,  0);

  static List<Pt> moves = new ArrayList<Pt>();
  static {
    moves.add(RIGHT);
    moves.add(DOWN);
    moves.add(LEFT);
    moves.add(UP);
    moves.add(STAY);
  }

  static Map<Integer, Pt> integerToMove = new HashMap<Integer, Pt>();
  static {
    integerToMove.put(0, RIGHT);
    integerToMove.put(1, DOWN);
    integerToMove.put(2, LEFT);
    integerToMove.put(3, UP);
  }

  static Map<Character, Integer> directionToInteger = new HashMap<Character, Integer>();
  static Map<Integer, Character> integerToDirection = new HashMap<Integer, Character>();
  static {
    directionToInteger.put('>',  0 );
    integerToDirection.put( 0 , '>');
    directionToInteger.put('v',  1 );
    integerToDirection.put( 1 , 'v');
    directionToInteger.put('<',  2 );
    integerToDirection.put( 2 , '<');
    directionToInteger.put('^',  3 );
    integerToDirection.put( 3 , '^');
  }

  public static void main(String[] args) throws Exception {
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Expedition testExpedition1 = new Expedition(testRows, 1, 500);
    int test1 = testExpedition1.run();
    assert test1 == 18;
    Expedition testExpedition2 = new Expedition(testRows, 3, 500);
    int test2 = testExpedition2.run();
    assert test2 == 54;    

    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Expedition realExpedition1 = new Expedition(realRows, 1, 500);
    System.out.println("Day 24 part 1: " + realExpedition1.run());
    Expedition realExpedition2 = new Expedition(realRows, 3, 500);
    System.out.println("Day 24 part 2: " + realExpedition2.run());
  }

  private static class State implements Comparable<State> {
    Pt point;
    int legsRemaining;
    Expedition expedition;
    Pt currentGoal;

    State(Pt point, int legsRemaining, Expedition expedition) {
      this.point = point;
      this.legsRemaining = legsRemaining;
      this.expedition = expedition;
      currentGoal = ((legsRemaining % 2 == 0)
                     ? expedition.end
                     : expedition.start);
    }

    int heuristic() {
      int result = point.manhattanDistance(currentGoal);
      if (legsRemaining > 0) {
        result += (legsRemaining * expedition.legHeuristic);
      }
      return result;
    }

    @Override
    public boolean equals(Object otherObj) {
      State other = (State)otherObj;
      return (this.point.equals(other.point)
              && this.legsRemaining == other.legsRemaining);
    }

    @Override
    public int hashCode() {
      return (point.hashCode() << 2) + legsRemaining;
    }

    @Override
    public int compareTo(State other) {
      return Integer.signum(this.heuristic() - other.heuristic());
    }

    @Override
    public String toString() {
      return "State(" + point + ", " + legsRemaining + ")";
    }
  }

  private static class Expedition {
    Blizzards blizzards;
    int threshold;
    Pt start;
    Pt end;
    Set<Pt> ground;
    int legHeuristic;
    List<State> states;
    Set<State> nextStates;
    boolean running;

    Expedition(String[] rows, int legsTotal, int threshold) {
      blizzards = new Blizzards(rows);
      this.threshold = threshold;
      start = new Pt(1, 0);
      end = new Pt(blizzards.valleyWidth, blizzards.valleyHeight + 1);

      ground = new HashSet<Pt>();
      ground.add(start);
      ground.add(end);
      for (int y = 1; y <= blizzards.valleyHeight; y++) {
        for (int x = 1; x <= blizzards.valleyWidth; x++) {
          ground.add(new Pt(x, y));
        }
      }

      legHeuristic = start.manhattanDistance(end);

      states = new ArrayList<State>();
      State startingState = new State(start, legsTotal - 1, this);
      states.add(startingState);
      nextStates = new HashSet<State>();
    }

    void moveState(State state) {
      for (Pt move : moves) {
        Pt newPoint = state.point.add(move);
        if (blizzards.points.contains(newPoint) || !ground.contains(newPoint)) continue;
        if (newPoint.equals(state.currentGoal)) {
          nextStates.add(new State(newPoint, state.legsRemaining - 1, this));
          if (state.legsRemaining == 0) running = false;
        } else {
          nextStates.add(new State(newPoint, state.legsRemaining, this));
        }
      }
    }

    void moveStates() {
      int maxStates = threshold;
      if (states.size() < threshold) maxStates = states.size();
      for (int i = 0; i < maxStates; i++) {
        moveState(states.get(i));
      }
      states.clear();
      states.addAll(nextStates);
      Collections.sort(states);
      nextStates.clear();
    }

    int run() {
      running = true;
      int minutes = 0;
      while (running) {
      // while (minutes < 2) {
        minutes++;
        blizzards.move();
        moveStates();
      }
      return minutes;
    }
  }

  private static class Blizzards {
    Set<Pt> points;
    Set<Pt3> pointsWithDirection;
    int valleyHeight;
    int valleyWidth;

    Blizzards(String[] rows) {
      valleyHeight = rows.length - 2;
      valleyWidth = rows[0].length() - 2;

      points = new HashSet<Pt>();
      pointsWithDirection = new HashSet<Pt3>();

      for (int y = 1; y <= valleyHeight; y++) {
        for (int x = 1; x <= valleyWidth; x++) {
          Integer z = directionToInteger.get(rows[y].charAt(x));
          if (z != null) {
            points.add(new Pt(x, y));
            pointsWithDirection.add(new Pt3(x, y, z));
          }
        }
      }
    }

    void move() {
      Set<Pt> newPoints = new HashSet<Pt>();
      Set<Pt3> newPointsWithDirection = new HashSet<Pt3>();

      for (Pt3 pt3 : pointsWithDirection) {
        Pt move = integerToMove.get(pt3.z());
        Pt newPoint = (new Pt(pt3.x(), pt3.y())).add(move);
        if (newPoint.x() == 0) {
          newPoint = new Pt(valleyWidth, newPoint.y());
        } else if (newPoint.x() == valleyWidth + 1) {
          newPoint = new Pt(1, newPoint.y());
        } else if (newPoint.y() == 0) {
          newPoint = new Pt(newPoint.x(), valleyHeight);
        } else if (newPoint.y() == valleyHeight + 1) {
          newPoint = new Pt(newPoint.x(), 1);
        }

        newPoints.add(newPoint);
        newPointsWithDirection.add(new Pt3(newPoint.x(), newPoint.y(), pt3.z()));
      }

      points.clear();
      pointsWithDirection.clear();
      points.addAll(newPoints);
      pointsWithDirection.addAll(newPointsWithDirection);
    }

    @Override
    public String toString() {
      Map<Pt, Character> pointToDirection = new HashMap<Pt, Character>();
      Character counter;
      for (Pt3 pt3 : pointsWithDirection) {
        Pt point = new Pt(pt3.x(), pt3.y());
        counter = pointToDirection.get(point);
        if (counter == null) {
          pointToDirection.put(point, integerToDirection.get(pt3.z()));
          continue;
        } else if (directionToInteger.containsKey(counter)) {
          pointToDirection.put(point, '2');
        } else {
          pointToDirection.put(point, ++counter);
        }
      }

      StringBuilder result = new StringBuilder();
      Character c;

      result.append("#.");
      for (int i = 0; i < valleyWidth; i++) {
        result.append('#');
      }
      result.append("\n");
      
      for (int y = 1; y <= valleyHeight; y++) {
        result.append("#");
      
        for (int x = 1; x <= valleyWidth; x++) {
          c = pointToDirection.get(new Pt(x, y));
          if (c != null) {
            result.append(c);
          } else {
            result.append('.');
          }
        }
      
        result.append("#\n");
      }
      
      for (int i = 0; i < valleyWidth; i++) {
        result.append('#');
      }
      result.append(".#\n");
      
      return result.toString();
    }
  }
}
