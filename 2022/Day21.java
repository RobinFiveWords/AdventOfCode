import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class Day21 {
  static String INPUT_FILE = "2022day21input.txt";
  static String TEST_INPUT_FILE = "2022day21testinput.txt";

  public static void main(String[] args) throws Exception {
    Map<String, Node> testNodes = new HashMap<String, Node>();
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    for (String row : testRows) {
      Node node = new Node(row);
      testNodes.put(node.name, node);
    }
    long test1 = testNodes.get("root").value(testNodes);
    assert test1 == 152;

    List<String> testPath = getPath("humn", testNodes);
    long testTarget = 0L;
    for (int i = testPath.size() - 2; i >= 0; i--) {
      Node currentParent = testNodes.get(testPath.get(i+1));
      testTarget = currentParent.newTarget(testTarget, testPath.get(i), testNodes);
    }
    assert testTarget == 301;

    Map<String, Node> realNodes = new HashMap<String, Node>();
    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    for (String row : realRows) {
      Node node = new Node(row);
      realNodes.put(node.name, node);
    }
    System.out.println("Day 21 part 1: " + realNodes.get("root").value(realNodes));
    
    List<String> realPath = getPath("humn", realNodes);
    long realTarget = 0L;
    for (int i = realPath.size() - 2; i >= 0; i--) {
      Node currentParent = realNodes.get(realPath.get(i+1));
      realTarget = currentParent.newTarget(realTarget, realPath.get(i), realNodes);
    }
    System.out.println("Day 21 part 2: " + realTarget);
  }

  private static List<String> getPath(String leaf, Map<String, Node> nodes) {
    List<String> results = new ArrayList<String>();
    String current = leaf;
    while (!current.equals("root")) {
      results.add(current);
      current = nodes.get(current).parent;
    }
    results.add("root");
    return results;
  }

  private static class Node {
    private String name;
    private Long value;
    private String leftChild;
    private String op;
    private String rightChild;
    public String parent;

    Node(String s) {
      String[] tokens = s.replace(":", "").split(" ");
      this.name = tokens[0];
      if (tokens.length == 2) {
        this.value = Long.parseLong(tokens[1]);
      } else {
        this.leftChild = tokens[1];
        this.op = tokens[2];
        this.rightChild = tokens[3];
      }
    }

    public long value(Map<String, Node> nodes) {
      if (value == null) {
        Node leftNode = nodes.get(leftChild);
        Node rightNode = nodes.get(rightChild);
        leftNode.parent = name;
        rightNode.parent = name;
        long leftValue = leftNode.value(nodes);
        long rightValue = rightNode.value(nodes);
        switch (op) {
          case "+":
            value = leftValue + rightValue;
            break;
          case "-":
            value = leftValue - rightValue;
            break;
          case "*":
            value = leftValue * rightValue;
            break;
          case "/":
            value = leftValue / rightValue;
            break;
        }
      }
      return value;
    }

    public long newTarget(long target, String child, Map<String, Node> nodes) {
      boolean left = (child.equals(leftChild));
      long otherValue = (left ? nodes.get(this.rightChild).value(nodes)
                              : nodes.get(this.leftChild).value(nodes));
      if (name.equals("root")) return otherValue;
      switch (op) {
        case "+": return target - otherValue;
        case "-": return left ? target + otherValue : otherValue - target;
        case "*": return target / otherValue;
        case "/": return left? target * otherValue : otherValue / target;
      }
      return 0L;  // Unreachable.
    }

    @Override
    public String toString() {
      String result = "Node(" + name + ": ";
      if (op == null) {
        return result + value + ")";
      } else {
        return result + leftChild + " " + op + " " + rightChild + ")";
      }
    }
  }
}