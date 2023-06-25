import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Day19 {
  static String INPUT_FILE = "2022day19input.txt";
  static String TEST_INPUT_FILE = "2022day19testinput.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    List<Blueprint> testBlueprints1 = parseBlueprints(testData);
    for (Blueprint blueprint : testBlueprints1) {
      blueprint.run(24, 10000);
    }
    assert testBlueprints1.get(0).qualityScore(24) == 9;
    assert testBlueprints1.get(1).qualityScore(24) == 24;
    List<Blueprint> testBlueprints2 = parseBlueprints(testData);
    for (Blueprint blueprint : testBlueprints2) {
      blueprint.run(32, 5000);
    }
    assert testBlueprints2.get(0).maxGeodes.get(32) == 56;
    assert testBlueprints2.get(1).maxGeodes.get(32) == 62;

    int real1 = 0;
    int real2 = 1;
    String[] realData = aocUtils.bufferLinesFromFile(INPUT_FILE);
    List<Blueprint> realBlueprints1 = parseBlueprints(realData);
    for (Blueprint blueprint : realBlueprints1) {
      blueprint.run(24, 10000);
      real1 += blueprint.qualityScore(24);
    }
    System.out.println("Day 19 part 1: " + real1);
    List<Blueprint> realBlueprints2 = parseBlueprints(realData, 3);
    for (Blueprint blueprint : realBlueprints2) {
      blueprint.run(32, 5000);
      real2 *= blueprint.maxGeodes.get(32);
    }
    System.out.println("Day 19 part 2: " + real2);
  }

  private static class State implements Comparable<State> {
    private int timeRemaining;
    private int oreRobots;
    private int oreInventory;
    private int clayRobots;
    private int clayInventory;
    private int obsidianRobots;
    private int obsidianInventory;
    private int geodeRobots;
    private int geodeInventory;

    State(int timeRemaining) {
      this.timeRemaining = timeRemaining;
      this.oreRobots = 1;
      this.oreInventory = 0;
      this.clayRobots = 0;
      this.clayInventory = 0;
      this.obsidianRobots = 0;
      this.obsidianInventory = 0;
      this.geodeRobots = 0;
      this.geodeInventory = 0;
    }

    State(int timeRemaining,
          int oreRobots,
          int oreInventory,
          int clayRobots,
          int clayInventory,
          int obsidianRobots,
          int obsidianInventory,
          int geodeRobots,
          int geodeInventory) {
      this.timeRemaining = timeRemaining;
      this.oreRobots = oreRobots;
      this.oreInventory = oreInventory;
      this.clayRobots = clayRobots;
      this.clayInventory = clayInventory;
      this.obsidianRobots = obsidianRobots;
      this.obsidianInventory = obsidianInventory;
      this.geodeRobots = geodeRobots;
      this.geodeInventory = geodeInventory;
    }

    @Override
    public int hashCode() {
      return (int)(timeRemaining
                   + (oreRobots << 8)
                   + (oreInventory << 11)
                   + (clayRobots << 14)
                   + (clayInventory << 17)
                   + (obsidianRobots << 20)
                   + (obsidianInventory << 23)
                   + (geodeRobots << 26)
                   + (geodeInventory << 29));
    }

    @Override
    public boolean equals(Object other) {
      State otherState = (State)other;
      return (this.timeRemaining == otherState.timeRemaining
              && this.oreRobots == otherState.oreRobots
              && this.oreInventory == otherState.oreInventory
              && this.clayRobots == otherState.clayRobots
              && this.clayInventory == otherState.clayInventory
              && this.obsidianRobots == otherState.obsidianRobots
              && this.obsidianInventory == otherState.obsidianInventory
              && this.geodeRobots == otherState.geodeRobots
              && this.geodeInventory == otherState.geodeInventory);
    }

    @Override
    public int compareTo(State other) {
      // We want to sort from best to worst, i.e., descending order
      // so that we can start on the best states and stop after whatever threshold we set.
      // If `this` is better than `other`, return -1; etc.
      int result;
      if ((result = Integer.signum(other.geodeRobots - this.geodeRobots)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.obsidianRobots - this.obsidianRobots)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.geodeInventory - this.geodeInventory)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.obsidianInventory - this.obsidianInventory)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.clayRobots - this.clayRobots)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.clayInventory - this.clayInventory)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.oreRobots - this.oreRobots)) != 0) {
        return result;
      } else if ((result = Integer.signum(other.oreInventory - this.oreInventory)) != 0) {
        return result;
      } else {
        return 0;
      }
    }

    State transformState(String action, Blueprint blueprint) {
      int newOreRobots = oreRobots;
      int newOreInventory = oreInventory;
      int newClayRobots = clayRobots;
      int newClayInventory = clayInventory;
      int newObsidianRobots = obsidianRobots;
      int newObsidianInventory = obsidianInventory;
      int newGeodeRobots = geodeRobots;
      int newGeodeInventory = geodeInventory;

      if (action == "ore") {
        newOreInventory = oreInventory - blueprint.oreCostOre;
        if (newOreInventory < 0) return null;
        newOreRobots = oreRobots + 1;
      } else if (action == "clay") {
        newOreInventory = oreInventory - blueprint.clayCostOre;
        if (newOreInventory < 0) return null;
        newClayRobots = clayRobots + 1;
      } else if (action == "obsidian") {
        newOreInventory = oreInventory - blueprint.obsidianCostOre;
        newClayInventory = clayInventory - blueprint.obsidianCostClay;
        if (newOreInventory < 0 || newClayInventory < 0) return null;
        newObsidianRobots = obsidianRobots + 1;
      } else if (action == "geode") {
        newOreInventory = oreInventory - blueprint.geodeCostOre;
        newObsidianInventory = obsidianInventory - blueprint.geodeCostObsidian;
        if (newOreInventory < 0 || newObsidianInventory < 0) return null;
        newGeodeRobots = geodeRobots + 1;
      }
      // else: pass

      newOreInventory += oreRobots;
      newClayInventory += clayRobots;
      newObsidianInventory += obsidianRobots;
      newGeodeInventory += geodeRobots;

      return new State(timeRemaining - 1,
                       newOreRobots,
                       newOreInventory,
                       newClayRobots,
                       newClayInventory,
                       newObsidianRobots,
                       newObsidianInventory,
                       newGeodeRobots,
                       newGeodeInventory);
    }

    @Override
    public String toString() {
      return ("State(timeRemaining=" + timeRemaining + "\n       "
              + "oreRobots=" + oreRobots + "\n       "
              + "oreInventory=" + oreInventory + "\n       "
              + "clayRobots=" + clayRobots + "\n       "
              + "clayInventory=" + clayInventory + "\n       "
              + "obsidianRobots=" + obsidianRobots + "\n       "
              + "obsidianInventory=" + obsidianInventory + "\n       "
              + "geodeRobots=" + geodeRobots + "\n       "
              + "geodeInventory=" + geodeInventory + "\n");
    }
  }

  private static class Blueprint {
    private static String[] actions = {"ore", "clay", "obsidian", "geode", "pass"};

    private int number;

    private int oreCostOre;
    private int clayCostOre;
    private int obsidianCostOre;
    private int obsidianCostClay;
    private int geodeCostOre;
    private int geodeCostObsidian;

    private List<Integer> maxGeodes;
    private Set<State> visited;
    private List<State> working;
    private Set<State> workingNext;

    Blueprint(int[] inputs) {
      this.number = inputs[0];
      this.oreCostOre = inputs[1];
      this.clayCostOre = inputs[2];
      this.obsidianCostOre = inputs[3];
      this.obsidianCostClay = inputs[4];
      this.geodeCostOre = inputs[5];
      this.geodeCostObsidian = inputs[6];

      this.maxGeodes = new ArrayList<Integer>();
      maxGeodes.add(0);

      working = new ArrayList<State>();
      workingNext = new HashSet<State>();
    }

    int qualityScore(int minutes) { return number * maxGeodes.get(minutes); }

    void run(int totalMinutes, int pruneStates) {
      State startingState = new State(totalMinutes);
      working.add(startingState);

      for (int currentMinutes = 0; currentMinutes < totalMinutes; currentMinutes++) {
        int currentMaxGeodes = 0;
        int stateIndex = 0;
        int maxStates = working.size();
        if (pruneStates < maxStates) maxStates = pruneStates;
        while (stateIndex < maxStates) {
          State currentState = working.get(stateIndex);
          for (String action : actions) {
            State newState = currentState.transformState(action, this);
            if (newState != null) {
              workingNext.add(newState);
              if (newState.geodeInventory > currentMaxGeodes) {
                currentMaxGeodes = newState.geodeInventory;
              }
            }
          }
          stateIndex++;
        }

        maxGeodes.add(currentMaxGeodes);

        working.clear();
        working.addAll(workingNext);
        Collections.sort(working);
        workingNext.clear();
      }
    }

    @Override
    public String toString() {
      return ("Blueprint " + number + ":\n  "
              + "Ore cost: " + oreCostOre + " ore\n  "
              + "Clay cost: " + clayCostOre + " ore\n  "
              + "Obsidian cost: " + obsidianCostOre + " ore + " + obsidianCostClay + " clay\n  "
              + "Geode cost: " + geodeCostOre + " ore + " + geodeCostObsidian + " obsidian\n");
    }
  }

  private static Blueprint parseRow(String row) {
    return new Blueprint(aocUtils.parseInts(row));
  }

  private static List<Blueprint> parseBlueprints(String[] rows) {
    List<Blueprint> results = new ArrayList<Blueprint>();
    for (String row : rows) {
      results.add(parseRow(row));
    }
    return results;
  }

  private static List<Blueprint> parseBlueprints(String[] rows, int maxRows) {
    List<Blueprint> results = new ArrayList<Blueprint>();
    for (int i = 0; i < maxRows; i++) {
      results.add(parseRow(rows[i]));
    }
    return results;
  }
}