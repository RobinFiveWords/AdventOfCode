import java.lang.Math;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class Day22 {
  static String INPUT_FILE = "2022day22input.txt";
  static String TEST_INPUT_FILE = "2022day22testinput.txt";

  static Pt right = new Pt( 1,  0);  // 0
  static Pt down  = new Pt( 0,  1);  // 1
  static Pt left  = new Pt(-1,  0);  // 2
  static Pt up    = new Pt( 0, -1);  // 3
  // R -> (current + 1) mod 4
  // L -> (current - 1) mod 4

  public static void main(String[] args) throws Exception {
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Set<Pt> testTiles = getPoints(testRows, '.');
    Set<Pt> testWalls = getPoints(testRows, '#');
    String[] testInstructions = parseInstructions(testRows[testRows.length - 1]);

    Map<Pt3, Pt3> testWraps1 = makeTestWraps1();
    Pt3 testPoint1 = processInstructions(testInstructions, testTiles, testWalls, testWraps1);
    assert password(testPoint1) == 6032;

    Map<Pt3, Pt3> testWraps2 = makeTestWraps2();
    Pt3 testPoint2 = processInstructions(testInstructions, testTiles, testWalls, testWraps2);
    assert password(testPoint2) == 5031;

    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Set<Pt> realTiles = getPoints(realRows, '.');
    Set<Pt> realWalls = getPoints(realRows, '#');
    String[] realInstructions = parseInstructions(realRows[realRows.length - 1]);

    Map<Pt3, Pt3> realWraps1 = makeRealWraps1();
    Pt3 realPoint1 = processInstructions(realInstructions, realTiles, realWalls, realWraps1);
    System.out.println("Day 22 part 1: " + password(realPoint1));

    Map<Pt3, Pt3> realWraps2 = makeRealWraps2();
    Pt3 realPoint2 = processInstructions(realInstructions, realTiles, realWalls, realWraps2);
    System.out.println("Day 22 part 2: " + password(realPoint2));
  }

  private static Pt3 processInstructions(String[] instructions, Set<Pt> tiles, Set<Pt> walls, Map<Pt3, Pt3> wraps) {
    Pt3 currentPoint = getStartingPoint(tiles);
    for (String instruction : instructions) {
      if (instruction.equals("R") || instruction.equals("L")) {
        currentPoint = rotatePoint(currentPoint, instruction);
        } else {
        for (int i = 0; i < Integer.parseInt(instruction); i++) {
          Pt3 newPoint = movePoint(currentPoint, tiles, walls, wraps);
          if (newPoint.equals(currentPoint)) break;  // if hit wall, move immediatly to next instruction
          currentPoint = newPoint;
        }
      }
    }
    return currentPoint;
  }

  // test layout
  //
  //   X
  // XXX
  //   XX

  private static Map<Pt3, Pt3> makeTestWraps1() {
    Map<Pt3, Pt3> results = new HashMap<Pt3, Pt3>();
    for (int y = 0; y < 4; y++) {
      results.put(new Pt3(8, y, 2), new Pt3(11, y, 2));
      results.put(new Pt3(11, y, 0), new Pt3(8, y, 0));
    }
    for (int y = 4; y < 8; y++) {
      results.put(new Pt3(0, y, 2), new Pt3(11, y, 2));
      results.put(new Pt3(11, y, 0), new Pt3(0, y, 0));
    }
    for (int y = 8; y < 12; y++) {
      results.put(new Pt3(8, y, 2), new Pt3(15, y, 2));
      results.put(new Pt3(15, y, 0), new Pt3(8, y, 0));
    }
    for (int x = 0; x < 8; x++) {
      results.put(new Pt3(x, 4, 3), new Pt3(x, 7, 3));
      results.put(new Pt3(x, 7, 1), new Pt3(x, 4, 1));
    }
    for (int x = 8; x < 12; x++) {
      results.put(new Pt3(x, 0, 3), new Pt3(x, 11, 3));
      results.put(new Pt3(x, 11, 1), new Pt3(x, 0, 1));
    }
    for (int x = 12; x < 16; x++) {
      results.put(new Pt3(x, 8, 3), new Pt3(x, 11, 3));
      results.put(new Pt3(x, 11, 1), new Pt3(x, 8, 1));
    }
    return results;
  }

  private static Map<Pt3, Pt3> makeTestWraps2() {
    Map<Pt3, Pt3> results = new HashMap<Pt3, Pt3>();
    for (int i = 0; i < 4; i++) {
      // (8, 0-3) left goes to (4-7, 4) down
      results.put(new Pt3(8, 0+i, 2), new Pt3(4+i, 4, 1));
      results.put(new Pt3(4+i, 4, 3), new Pt3(8, 0+i, 0));
      // (8, 8-11) left goes to (7-4, 7) up
      results.put(new Pt3(8, 0+i, 2), new Pt3(7-i, 7, 3));
      results.put(new Pt3(7-1, 7, 1), new Pt3(8, 0+i, 0));
      // (11, 4-7) right goes to (15-12, 8) down
      results.put(new Pt3(11, 4+i, 0), new Pt3(15-i, 8, 1));
      results.put(new Pt3(15-i, 8, 3), new Pt3(11, 4+i, 2));
      // (0-3, 7) down goes to (11-8, 11) up
      results.put(new Pt3(0+i, 7, 1), new Pt3(11-i, 11, 3));
      results.put(new Pt3(11-i, 11, 1), new Pt3(0+i, 7, 3));
      // (0, 7-4) left goes to (12-15, 11) up
      results.put(new Pt3(0, 7-i, 2), new Pt3(12+i, 11, 3));
      results.put(new Pt3(12+i, 11, 1), new Pt3(0, 7-i, 0));
      // (11, 0-3) right goes to (15, 11-8) left
      results.put(new Pt3(11, 0+i, 0), new Pt3(15, 11-i, 2));
      results.put(new Pt3(15, 11-i, 0), new Pt3(11, 0+1, 2));
      // (3-0, 4) up goes to (8-11, 0) down
      results.put(new Pt3(3-i, 4, 3), new Pt3(8+i, 0, 1));
      results.put(new Pt3(8+i, 0, 3), new Pt3(3-i, 4, 1));
    }
    return results;
  }

  // my real layout
  //
  //  XX
  //  X
  // XX
  // X

  private static Map<Pt3, Pt3> makeRealWraps1() {
    Map<Pt3, Pt3> results = new HashMap<Pt3, Pt3>();
    for (int y = 0; y < 50; y++) {
      results.put(new Pt3(50, y, 2), new Pt3(149, y, 2));
      results.put(new Pt3(149, y, 0), new Pt3(50, y, 0));
    }
    for (int y = 50; y < 100; y++) {
      results.put(new Pt3(50, y, 2), new Pt3(99, y, 2));
      results.put(new Pt3(99, y, 0), new Pt3(50, y, 0));
    }
    for (int y = 100; y < 150; y++) {
      results.put(new Pt3(0, y, 2), new Pt3(99, y, 2));
      results.put(new Pt3(99, y, 0), new Pt3(0, y, 0));
    }
    for (int y = 150; y < 200; y++) {
      results.put(new Pt3(0, y, 2), new Pt3(49, y, 2));
      results.put(new Pt3(49, y, 0), new Pt3(0, y, 0));
    }
    for (int x = 0; x < 50; x++) {
      results.put(new Pt3(x, 100, 3), new Pt3(x, 199, 3));
      results.put(new Pt3(x, 199, 1), new Pt3(x, 100, 1));
    }
    for (int x = 50; x < 100; x++) {
      results.put(new Pt3(x, 0, 3), new Pt3(x, 149, 3));
      results.put(new Pt3(x, 149, 1), new Pt3(x, 0, 1));
    }
    for (int x = 100; x < 150; x++) {
      results.put(new Pt3(x, 0, 3), new Pt3(x, 49, 3));
      results.put(new Pt3(x, 49, 1), new Pt3(x, 0, 1));
    }
    return results;
  }

  private static Map<Pt3, Pt3> makeRealWraps2() {
    Map<Pt3, Pt3> results = new HashMap<Pt3, Pt3>();
    for (int i = 0; i < 50; i++) {
      // (49-0, 100) up goes to (50, 99-50) right
      results.put(new Pt3(49-i, 100, 3), new Pt3(50, 99-i, 0));
      results.put(new Pt3(50, 99-i, 2), new Pt3(49-i, 100, 1));
      // (0, 100-149) left goes to 50, 49-0) right
      results.put(new Pt3(0, 100+i, 2), new Pt3(50, 49-i, 0));
      results.put(new Pt3(50, 49-i, 2), new Pt3(0, 100+i, 0));
      // (0, 150-199) left goes to (50-99, 0) down
      results.put(new Pt3(0, 150+i, 2), new Pt3(50+i, 0, 1));
      results.put(new Pt3(50+i, 0, 3), new Pt3(0, 150+i, 0));
      // (0-49, 199) down goes to (100-149, 0) down
      results.put(new Pt3(0+i, 199, 1), new Pt3(100+i, 0, 1));
      results.put(new Pt3(100+i, 0, 3), new Pt3(0+i, 199, 3));
      // (49, 199-150) right goes to (99-50, 149) up
      results.put(new Pt3(49, 199-i, 0), new Pt3(99-i, 149, 3));
      results.put(new Pt3(99-i, 149, 1), new Pt3(49, 199-i, 2));
      // (99, 99-50) right goes to (149-100, 49) up
      results.put(new Pt3(99, 99-i, 0), new Pt3(149-i, 49, 3));
      results.put(new Pt3(149-i, 49, 1), new Pt3(99, 99-i, 2));
      // (99, 149-100) right goes to (149, 0-49) left
      results.put(new Pt3(99, 149-i, 0), new Pt3(149, 0+i, 2));
      results.put(new Pt3(149, 0+i, 0), new Pt3(99, 149-i, 2));
    }
    return results;
  }

  private static Pt3 getStartingPoint(Set<Pt> points) {
    int minX = Integer.MAX_VALUE;
    for (Pt point : points) {
      if (point.y() == 0) {
        int x;
        if ((x = point.x()) < minX) minX = x;
      }
    }
    return new Pt3(minX, 0, 0);
  }

  private static Pt3 movePoint(Pt3 point, Set<Pt> tiles, Set<Pt> walls, Map<Pt3, Pt3> wraps) {
    Pt newXY;
    switch (point.z()) {
      case 0:  // right
        newXY = new Pt(point.x(), point.y()).add(right);
        break;
      case 1:  // down
        newXY = new Pt(point.x(), point.y()).add(down);
        break;
      case 2:  // left
        newXY = new Pt(point.x(), point.y()).add(left);
        break;
      case 3:  // up
        newXY = new Pt(point.x(), point.y()).add(up);
        break;
      default:  // Unreachable.
        newXY = new Pt(0, 0);
    }
    if (tiles.contains(newXY)) return new Pt3(newXY.x(), newXY.y(), point.z());
    if (walls.contains(newXY)) return point;
    Pt3 newXYZ = wraps.get(point);
    Pt newXYw = new Pt(newXYZ.x(), newXYZ.y());
    if (walls.contains(newXYw)) return point;
    assert tiles.contains(newXYw);
    return newXYZ;
  }

  private static Pt3 rotatePoint(Pt3 point, String turn) {
    int newDirection = Math.floorMod(point.z() + (turn.equals("R") ? 1 : -1), 4);
    return new Pt3(point.x(), point.y(), newDirection);
  }

  private static Set<Pt> getPoints(String[] rows, char c) {
    Set<Pt> results = new HashSet<Pt>();
    for (int y = 0; y < rows.length; y++) {
      int rowlen = rows[y].length();
      if (rowlen == 0) break;
      for (int x = 0; x < rowlen; x++) {
        if (rows[y].charAt(x) == c) results.add(new Pt(x, y));
      }
    }
    return results;
  }

  private static String[] parseInstructions(String s) {
    return s.split("((?<=[LR])|(?=[LR]))");
  }

  private static int password(Pt3 point) {
    return 1000 * (point.y() + 1) + 4 * (point.x() + 1) + point.z();
  }
}