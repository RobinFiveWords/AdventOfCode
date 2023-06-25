import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Day18 {
  static String INPUT_FILE = "2022day18input.txt";
  static String TEST_INPUT_FILE = "2022day18testinput.txt";

  static List<Pt3> directions = new ArrayList<Pt3>();
  static {
    directions.add(new Pt3(-1,  0,  0));
    directions.add(new Pt3( 1,  0,  0));
    directions.add(new Pt3( 0, -1,  0));
    directions.add(new Pt3( 0,  1,  0));
    directions.add(new Pt3( 0,  0, -1));
    directions.add(new Pt3( 0,  0,  1));
  }
  
  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Set<Pt3> testPoints = parseInput(testData);
    assert totalSurfaceArea(testPoints) == 64;
    assert exteriorSurfaceArea(testPoints) == 58;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Set<Pt3> realPoints = parseInput(realData);
    System.out.println("Day 18 part 1: " + totalSurfaceArea(realPoints));
    System.out.println("Day 18 part 2: " + exteriorSurfaceArea(realPoints));
  }

  private static Set<Pt3> parseInput(String[] data) {
    Set<Pt3> results = new HashSet<Pt3>();
    for (String row : data) {
      int[] coords = aocUtils.parseInts(row);
      Pt3 point = new Pt3(coords[0], coords[1], coords[2]);
      results.add(point);
    }
    return results;
  }

  private static int totalSurfaceArea(Set<Pt3> points) {
    int result = 0;
    for (Pt3 point : points) {
      result += 6;
      for (Pt3 direction : directions) {
        if (points.contains(point.add(direction))) result--;
      }
    }
    return result;
  }

  private static int exteriorSurfaceArea(Set<Pt3> points) {
    int xmin = 999;
    int xmax = 0;
    int ymin = 999;
    int ymax = 0;
    int zmin = 999;
    int zmax = 0;
    for (Pt3 point : points) {
      if (point.x() < xmin) xmin = point.x();
      if (point.x() > xmax) xmax = point.x();
      if (point.y() < ymin) ymin = point.y();
      if (point.y() > ymax) ymax = point.y();
      if (point.z() < zmin) zmin = point.z();
      if (point.z() > zmax) zmax = point.z();
    }
    xmin--;
    xmax++;
    ymin--;
    ymax++;
    zmin--;
    zmax++;

    int result = 0;
    Set<Pt3> visited = new HashSet<Pt3>();
    Queue<Pt3> queue = new Queue<Pt3>();
    Pt3 startingPoint = new Pt3(xmin, ymin, zmin);
    queue.enqueue(startingPoint);
    while (!queue.isEmpty()) {
      Pt3 currentPoint = queue.dequeue();
      if (visited.contains(currentPoint)) continue;
      visited.add(currentPoint);
      for (Pt3 direction : directions) {
        Pt3 nextPoint = currentPoint.add(direction);
        if (nextPoint.x() < xmin
            || nextPoint.x() > xmax
            || nextPoint.y() < ymin
            || nextPoint.y() > ymax
            || nextPoint.z() < zmin
            || nextPoint.z() > zmax) continue;
        if (visited.contains(nextPoint)) continue;
        if (points.contains(nextPoint)) {
          result++;
          continue;
        }
        queue.enqueue(nextPoint);
      }
    }
    return result;
  }
}