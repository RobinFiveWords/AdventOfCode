import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.Set;

public class Day15 {
  static String TEST_INPUT_FILE = "2022day15testinput.txt";
  static String INPUT_FILE = "2022day15input.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Map<PtL, PtL> testPairs = parseInput(testData);
    assert ruledOut(testPairs, 10L) == 26L;
    Map<PtL, Long> testSensors = getSensors(testPairs);
    assert tuningFrequency(findDistress(testSensors, 0L, 20L)) == 56000011L;
    assert tuningFrequency(findDistress2(testSensors, 0L, 20L)) == 56000011L;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Map<PtL, PtL> realPairs = parseInput(realData);
    System.out.println("Day 15 part 1: " + ruledOut(realPairs, 2000000L));
    Map<PtL, Long> realSensors = getSensors(realPairs);
    System.out.println("Day 15 part 2: " +
        tuningFrequency(findDistress(realSensors, 0L, 4000000L)));
    System.out.println("Day 15 part 2 faster: " +
        tuningFrequency(findDistress2(realSensors, 0L, 4000000L)));
  }

  private static int[] parseInts(String s) {
    List<Integer> results = new ArrayList<Integer>();
    Matcher m = Pattern.compile("-?\\d+").matcher(s);
    while (m.find()) {
        results.add(Integer.parseInt(m.group()));
    }
    int[] arr = results.stream().mapToInt(i->i).toArray();
    return arr;
  }

  private static Map<PtL, PtL> parseInput(String[] data) {
    Map<PtL, PtL> results = new HashMap<PtL, PtL>();
    for (String row : data) {
      int[] numbers = parseInts(row);
      PtL sensor = new PtL(numbers[0], numbers[1]);
      PtL beacon = new PtL(numbers[2], numbers[3]);
      results.put(sensor, beacon);
    }
    return results;
  }

  private static Map<PtL, Long> getSensors(Map<PtL, PtL> pairs) {
    Map<PtL, Long> results = new HashMap<PtL, Long>();
    for (Map.Entry<PtL, PtL> pair : pairs.entrySet()) {
      PtL sensor = pair.getKey();
      PtL beacon = pair.getValue();
      long distance = sensor.manhattanDistance(beacon);
      results.put(sensor, distance);
    }
    return results;
  }

  private static boolean outsideAll(PtL point, Map<PtL, Long> sensors) {
    for (Map.Entry<PtL, Long> pair : sensors.entrySet()) {
      PtL sensor = pair.getKey();
      long distance = pair.getValue();
      if (distance >= sensor.manhattanDistance(point)) return false;
    }
    return true;
  }

  private static long tuningFrequency(PtL point) {
    return point.x() * 4000000L + point.y();
  }

  private static class Line {
    private final PtL p1;
    private final PtL p2;

    Line(PtL p1, PtL p2) {
      this.p1 = p1;
      this.p2 = p2;

      // ensure p1 is not right of p2
      if (this.p1.x() > this.p2.x()) {
        PtL tmp = p1;
        p1 = p2;
        p2 = tmp;
      }
    }

    private boolean rising() {
      return (p2.x() > p1.x()) == (p2.y() > p1.y());
    }

    public PtL intersection(Line other) {
      if (rising() == other.rising()) return null;
      Line l1 = this;
      Line l2 = other;
      if (rising()) {
        Line tmp = l1;
        l1 = l2;
        l2 = tmp;
      }
      // now l2 is definitely the rising one
      long b1 = l1.p1.x() + l1.p1.y(); // not rising: y-intercept is sum of coords
      long b2 = l2.p1.y() - l2.p1.x(); // rising: y-intercept is difference of coords
      if ((b1 + b2) % 2L == 1L) return null; // this isn't going to give us a single possibility
      long target_y = (b1 + b2) / 2;
      long target_x = (b1 - b2) / 2;
      if (l1.p1.x() <= target_x && target_x <= l1.p2.x() &&
          l1.p2.y() <= target_y && target_y <= l1.p1.y() &&
          l2.p1.x() <= target_x && target_x <= l2.p2.x() &&
          l2.p1.x() <= target_y && target_y <= l2.p2.y()) {
        return new PtL(target_x, target_y);
      }
      return null;
    }
  }

  private static List<Line> getFringe(PtL sensor, Long distance) {
    long targetDistance = distance + 1;
    long x = sensor.x();
    long y = sensor.y();
    List<Line> results = new ArrayList<Line>();
    results.add(new Line(new PtL(x - targetDistance, y),
                         new PtL(x, y + targetDistance)));
    results.add(new Line(new PtL(x, y + targetDistance),
                         new PtL(x + targetDistance, y)));
    results.add(new Line(new PtL(x + targetDistance, y),
                         new PtL(x, y - targetDistance)));
    results.add(new Line(new PtL(x, y - targetDistance),
                         new PtL(x - targetDistance, y)));
    return results;
  }

  private static PtL findDistress(Map<PtL, Long> sensors, long min, long max) {
    List<List<Line>> fringes = new ArrayList<List<Line>>();
    for (Map.Entry<PtL, Long> pair : sensors.entrySet()) {
      PtL sensor = pair.getKey();
      Long distance = pair.getValue();
      fringes.add(getFringe(sensor, distance));
    }
    Set<PtL> candidates = new HashSet<PtL>();
    for (int i = 0; i < fringes.size() - 1; i++) {
      for (int j = i + 1; j < fringes.size(); j++) {
        for (Line l1 : fringes.get(i)) {
          for (Line l2 : fringes.get(j)) {
            PtL attempt = l1.intersection(l2);
            if (attempt != null) candidates.add(attempt);
          }
        }
      }
    }
    Set<PtL> results = new HashSet<PtL>();
    for (PtL candidate : candidates) {
      if (candidate.x() < min || candidate.x() > max ||
          candidate.y() < min || candidate.y() > max) continue;
      if (outsideAll(candidate, sensors)) {
        results.add(candidate);
      }
    }
    if (results.size() == 1) return results.iterator().next();
    return null;
  }

  private static PtL findDistress2(Map<PtL, Long> sensors, long min, long max) {
    Set<Long> candidatesRising = new HashSet<Long>();
    Set<Long> candidatesFalling = new HashSet<Long>();
    Set<Long> interceptsRising = new HashSet<Long>();
    Set<Long> interceptsFalling = new HashSet<Long>();

    for (Map.Entry<PtL, Long> pair : sensors.entrySet()) {
      PtL sensor = pair.getKey();
      long targetDistance = pair.getValue() + 1L;
      long risingAbove = sensor.y() + targetDistance - sensor.x();
      long risingBelow = sensor.y() - targetDistance - sensor.x();
      long fallingAbove = sensor.y() + targetDistance + sensor.x();
      long fallingBelow = sensor.y() - targetDistance + sensor.x();
      if (interceptsRising.contains(risingAbove)) {
        candidatesRising.add(risingAbove);
      } else {
        interceptsRising.add(risingAbove);
      }
      if (interceptsRising.contains(risingBelow)) {
        candidatesRising.add(risingBelow);
      } else {
        interceptsRising.add(risingBelow);
      }
      if (interceptsFalling.contains(fallingAbove)) {
        candidatesFalling.add(fallingAbove);
      } else {
        interceptsFalling.add(fallingAbove);
      }
       if (interceptsFalling.contains(fallingBelow)) {
        candidatesFalling.add(fallingBelow);
      } else {
        interceptsFalling.add(fallingBelow);
      }
    }

    Set<PtL> results = new HashSet<PtL>();
    for (long cR : candidatesRising) {
      for (long cF : candidatesFalling) {
        if (cR > cF) continue;
        PtL candidate = new PtL((cF - cR) / 2, (cF + cR) / 2);
        if (candidate.x() < min || candidate.x() > max ||
            candidate.y() < min || candidate.y() > max) continue;
        if (outsideAll(candidate, sensors)) {
          results.add(candidate);
        }
      }
    }
    if (results.size() == 1) return results.iterator().next();
    return null;
  }

  private static long ruledOut(Map<PtL, PtL> pairs, long y) {
    long result = 0;
    Set<Long> beaconXcounted = new HashSet<Long>();

    List<IntervalClosed> intervals = new ArrayList<IntervalClosed>();
    for (Map.Entry<PtL, PtL> pair : pairs.entrySet()) {
      PtL sensor = pair.getKey();
      PtL beacon = pair.getValue();
      long closeDistance = sensor.manhattanDistance(beacon);
      long targetDistance = Math.abs(sensor.y() - y);
      if (targetDistance > closeDistance) continue;

      // need to exclude where beacons are known to exist
      // and that X position will be within interval counted later
      if (beacon.y() == y && !beaconXcounted.contains(beacon.x())) {
        result--;
        beaconXcounted.add(beacon.x());
      }

      long remainingDistance = closeDistance - targetDistance;
      intervals.add(new IntervalClosed(sensor.x() - remainingDistance,
                                       sensor.x() + remainingDistance));
    }
    Collections.sort(intervals);

    boolean first = true;
    long workingStart = 0;
    long workingEnd = 0;
    for (IntervalClosed interval : intervals) {
      if (first) {
        workingStart = interval.start;
        workingEnd = interval.end;
        first = false;
      } else {
        if (interval.start > workingEnd + 1) {
          result += (workingEnd - workingStart + 1);
          workingStart = interval.start;
          workingEnd = interval.end;
        } else if (interval.end > workingEnd) {
          workingEnd = interval.end;
        }
      }
    }
    result += (workingEnd - workingStart + 1);
    return result;
  }

  private static class IntervalClosed implements Comparable<IntervalClosed> {
    private long start;
    private long end;

    public IntervalClosed(long start, long end) {
      this.start = start;
      this.end = end;
    }

    public IntervalClosed(int start, int end) {
      this.start = (long)start;
      this.end = (long)end;
    }

    @Override
    public int compareTo(IntervalClosed other) {
      int sign = (int)Long.signum(this.start - other.start);
      return (sign != 0) ? sign : (int)Long.signum(this.end - other.end);
    }

    @Override
    public String toString() {
      return "IntervalClosed(" + start + ", " + end + ")";
    }
  }
}