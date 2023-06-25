import java.lang.Math;
import java.util.Arrays;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Day16 {
  static String TEST_INPUT_FILE = "2022day16testinput.txt";
  static String INPUT_FILE = "2022day16input.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    Simulation testSim = new Simulation(testData);
    int test1 = testSim.run("AA", 30, false);
    assert test1 == 1651;
    int test2 = testSim.run("AA", 26, true);
    assert test2 == 1707;

    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    Simulation realSim = new Simulation(realData);
    int real1 = realSim.run("AA", 30, false);
    System.out.println("Day 16 part 1: " + real1);
    int real2 = realSim.run("AA", 26, true);
    System.out.println("Day 16 part 2: " + real2);
  }

  private static class Row {
    String valve;
    int flowRate;
    List<String> adjacentValves;

    Row(String s) {
      Matcher m = Pattern.compile("Valve ([A-Z]{2}) has flow rate=([0-9]+); "
                                  + "tunnels? leads? to valves? (.*)"
                                  ).matcher(s);
      m.find();
      valve = m.group(1);
      flowRate = Integer.parseInt(m.group(2));
      adjacentValves = Arrays.asList(m.group(3).split(", "));
    }

    public String toString() {
      String vs = "[" + String.join(", ", adjacentValves) + "]";
      return "Row("
               + String.join(", ", valve,
                                   Integer.toString(flowRate),
                                   vs)
               + ")";
    }
  }

  private static List<Row> parseRows(String[] data) {
    List<Row> results = new ArrayList<>();
    for (String s : data) {
      results.add(new Row(s));
    }
    return results;
  }

  private static Map<String, Set<String>> createAdjacencyList(List<Row> rows) {
    Map<String, Set<String>> results = new HashMap<>();
    for (Row row : rows) {
      Set<String> adjacent = new HashSet<>();
      for (String adjacentValve : row.adjacentValves) {
        adjacent.add(adjacentValve);
      }
      results.put(row.valve, adjacent);
    }
    return results;
  }

  private static Map<String, Integer> createFlowValves(List<Row> rows) {
    Map<String, Integer> results = new HashMap<>();
    for (Row row : rows) {
      if (row.flowRate > 0) {
        results.put(row.valve, row.flowRate);
      }
    }
    return results;
  }

  private static Map<String, Map<String, Integer>> getDistances(Map<String, Set<String>> adj) {
    Map<String, Map<String, Integer>> results = new HashMap<>();
    Set<String> allValves = adj.keySet();
    for (String v1 : allValves) {
      Map<String, Integer> initialDistances = new HashMap<>();
      for (String v2 : allValves) {
        if (adj.get(v1).contains(v2)) {
          initialDistances.put(v2, 1);
        } else {
          initialDistances.put(v2, adj.size());
        }
      }
      results.put(v1, initialDistances);
    }
    for (String k : allValves) {
      for (String i : allValves) {
        for (String j : allValves) {
          int ij = results.get(i).get(j);
          int ik = results.get(i).get(k);
          int kj = results.get(k).get(j);
          if (ik + kj < ij) {
            results.get(i).put(j, ik + kj);
          }
        }
      }
    }
    return results;
  }

  private static Map<String, Integer> getStateBitmask(Map<String, Integer> flows) {
    Map<String, Integer> results = new HashMap<>();
    int i = 0;
    for (String v : flows.keySet()) {
      results.put(v, 1 << i);
      i++;
    }
    return results;
  }

  private static class Simulation {
    private List<Row> rows;
    private Map<String, Set<String>> adj;
    private Map<String, Integer> flows;
    private Set<String> flowValves;
    private Map<String, Map<String, Integer>> distances;
    private Map<String, Integer> stateBitmask;
    private Map<Integer, Integer> results;

    public Simulation(String[] data) {
      rows = parseRows(data);
      adj = createAdjacencyList(rows);
      flows = createFlowValves(rows);
      flowValves = flows.keySet();
      distances = getDistances(adj);
      stateBitmask = getStateBitmask(flows);
    }

    private void visit(String currentValve, int timeRemaining, int state, int flow) {
      results.put(state, Math.max(results.getOrDefault(state, 0), flow));
      for (String nextValve : flowValves) {
        if ((stateBitmask.get(nextValve) & state) > 0) continue;
        int newTimeRemaining = (timeRemaining
                                - distances.get(currentValve).get(nextValve)
                                - 1);
        if (newTimeRemaining <= 0) continue;
        int newStateBitmask = state | stateBitmask.get(nextValve);
        int newFlow = flow + newTimeRemaining * flows.get(nextValve);
        visit(nextValve, newTimeRemaining, newStateBitmask, newFlow);
      }
    }

    public int run(String startingValve, int startingTime, Boolean elephant) {
      int answer = 0;
      results = new HashMap<>();
      visit(startingValve, startingTime, 0, 0);
      if (elephant) {
        for (Map.Entry<Integer, Integer> result1 : results.entrySet()) {
          int state1 = result1.getKey();
          for (Map.Entry<Integer, Integer> result2 : results.entrySet()) {
            int state2 = result2.getKey();
            if ((state1 & state2) == 0) {
              int combinedFlow = result1.getValue() + result2.getValue();
              answer = Math.max(answer, combinedFlow);
            }
          }
        }
      } else {
        for (int state : results.keySet()) {
          answer = Math.max(answer, results.get(state));
        }
      }
      return answer;
    }
  }
}