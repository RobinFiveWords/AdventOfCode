import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Day14 {
  static Pt down      = new Pt( 0,  1);
  static Pt downLeft  = new Pt(-1,  1);
  static Pt downRight = new Pt( 1,  1);

  public static void main(String[] args) throws Exception {
    String[] testData = new String[2];
    testData[0] = "498,4 -> 498,6 -> 496,6";
    testData[1] = "503,4 -> 502,4 -> 502,9 -> 494,9";

    String INPUT_FILE = "2022day14input.txt";

    Cave test1 = new Cave(testData, false);
    assert test1.run() == 24;
    Cave test2 = new Cave(testData, true);
    assert test2.run() == 93;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Cave real1 = new Cave(realData, false);
    System.out.println("Day 14 part 1: " + real1.run());
    Cave real2 = new Cave(realData, true);
    System.out.println("Day 14 part 2: " + real2.run());
  }

  private static Set<Pt> parseInput(String[] data) {
    Set<Pt> results = new HashSet<Pt>();
    for (String row : data) {
      results.addAll(parseRow(row));
    }
    return results;
  }

  private static Set<Pt> parseRow(String s) {
    List<Pt> points = new ArrayList<Pt>();
    String[] values = s.split(" -> ");
    for (String value : values) {
      String[] coords = value.split(",");
      points.add(new Pt(Integer.parseInt(coords[0]),
                        Integer.parseInt(coords[1])));
    }
    Set<Pt> results = new HashSet<Pt>();
    for (int i = 0; i < points.size() - 1; i++) {
      results.addAll(pointsInLine(points.get(i), points.get(i+1)));
    }
    return results;
  }

  private static Set<Pt> pointsInLine(Pt p1, Pt p2) {
    Set<Pt> results = new HashSet<Pt>();
    if (p1.x() == p2.x()) {
      // vertical
      int x = p1.x();
      int yStart = p1.y();
      int yEnd = p2.y();
      if (yEnd < yStart) {
        // reverse endpoints
        int tmp = yEnd;
        yEnd = yStart;
        yStart = tmp;
      }
      for (int i = yStart; i <= yEnd; i++) {
        results.add(new Pt(x, i));
      }
    } else if (p1.y() == p2.y()) {
      // horizontal
      int y = p1.y();
      int xStart = p1.x();
      int xEnd = p2.x();
      if (xEnd < xStart) {
        // reverse endpoints
        int tmp = xEnd;
        xEnd = xStart;
        xStart = tmp;
      }
      for (int i = xStart; i <= xEnd; i++) {
        results.add(new Pt(i, y));
      }
    } else {
      ;
    }
    return results;
  }

  private static class Cave {
    private Set<Pt> rocks;
    private int maxY;
    private Set<Pt> occupied;
    private Pt start = new Pt(500, 0);
    private Stack<Pt> path;
    private Pt sandPoint;

    Cave(String[] data, boolean floor) {
      rocks = parseInput(data);
      maxY = getMaxY();
      if (floor) {
        maxY += 2;
        rocks.addAll(pointsInLine(new Pt(500 - (maxY), maxY),
                                  new Pt(500 + (maxY), maxY)));
      }
      occupied = new HashSet<Pt>(rocks);
      path = new Stack<Pt>();
      path.push(start);
    }

    private int getMaxY() {
      int result = 0;
      for (Pt rock : rocks) {
        if (rock.y() > result) {
          result = rock.y();
        }
      }
      return result;
    }

    public int run() {
      while (!path.isEmpty()) {
        boolean abyss = fall();
        if (abyss) break;
      }
      return occupied.size() - rocks.size();
    }

    private void move(Pt newPoint) {
      path.push(sandPoint);
      sandPoint = newPoint;
    }

    private boolean fall() {
      sandPoint = path.pop();
      Pt newPoint;
      for (;;) {
        newPoint = sandPoint.add(down);
        if (!occupied.contains(newPoint)) {
          move(newPoint);
          if (newPoint.y() >= maxY) return true;
          continue;
        }
        newPoint = sandPoint.add(downLeft);
        if (!occupied.contains(newPoint)) {
          move(newPoint);
          if (newPoint.y() >= maxY) return true;
          continue;
        }
        newPoint = sandPoint.add(downRight);
        if (!occupied.contains(newPoint)) {
          move(newPoint);
          if (newPoint.y() >= maxY) return true;
          continue;
        }
        // comes to rest
        occupied.add(sandPoint);
        return false;
      }
    }
  }
}