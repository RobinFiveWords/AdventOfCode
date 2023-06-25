import java.lang.Math;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

class Day13 {
  static String TEST_INPUT_FILE = "2022day13testinput.txt";
  static String INPUT_FILE = "2022day13input.txt";

  static String DIVIDER_PACKET_1 = "[[2]]";
  static String DIVIDER_PACKET_2 = "[[6]]";

  public static void main(String[] args) throws Exception {
    String testData1 = aocUtils.readFileAsString(TEST_INPUT_FILE);
    int test1 = doPart1(testData1);
    assert test1 == 13;

    String[] testData2 = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    int test2 = doPart2(testData2);
    assert test2 == 140;

    String realData1 = aocUtils.readFileAsString(INPUT_FILE);
    int real1 = doPart1(realData1);
    System.out.println("Day 13 part 1: " + real1);

    String[] realData2 = aocUtils.bufferLinesFromFile(INPUT_FILE);
    int real2 = doPart2(realData2);
    System.out.println("Day 13 part 2: " + real2);
  }

  private static int doPart1(String s) {
    String[] pairs = s.split("\n\n");
    int result = 0;
    for (int i = 0; i < pairs.length; i++) {
      if (comparePackets(pairs[i]) == -1) {
        result += (i + 1);
      }
    }
    return result;
  }

  private static int doPart2(String[] arr) {
    List<Node> packets = new ArrayList<Node>();
    for (int i = 0; i < arr.length; i++) {
      if (arr[i].length() == 0) continue; // ignore blank lines
      packets.add(parsePacket(arr[i]));
    }
    Node divider1 = parsePacket(DIVIDER_PACKET_1);
    packets.add(divider1);
    Node divider2 = parsePacket(DIVIDER_PACKET_2);
    packets.add(divider2);

    Collections.sort(packets);
    int result = 1;
    for (int i = 0; i < packets.size(); i++) {
      // this check works with == or .equals()
      // because packets contains a reference to each packet / root node
      // if (packets.get(i).equals(divider1) || packets.get(i).equals(divider2)) {
      if (packets.get(i) == divider1 || packets.get(i) == divider2) {
        result *= (i + 1);
      }
    }
    return result;
  }

  private static int comparePackets(String s) {
    String[] pair = s.split("\n");
    assert pair.length == 2;
    Node n1 = parsePacket(pair[0]);
    Node n2 = parsePacket(pair[1]);
    return compareNodes(n1, n2);
  }

  private static Node parsePacket(String s) {
    Node root = new Node();
    Node currentNode = root;
    assert s.charAt(0) == '[';
    int i = 1; // start within root node
    while (i < s.length()) {
      if (s.charAt(i) == '[') {
        Node childNode = new Node(currentNode);
        currentNode = childNode;
        i++;
      } else if (s.charAt(i) == ']') {
        // end of node
        currentNode = currentNode.parent;
        i++;
      } else if (s.charAt(i) == ',') {
        i++;
      } else {
        // integer
        Matcher m = Pattern.compile("\\d+").matcher(s.substring(i));
        m.find();
        String childValue = m.group();
        Node childNode = new Node(currentNode);
        childNode.value = Integer.parseInt(childValue);
        i += childValue.length();
      }
    }
    return root;
  }

  private static int compareNodes(Node n1, Node n2) {
    if (n1.value != null && n2.value != null) {
      // both values are integers
      return Integer.signum(n1.value - n2.value); // -1 right order, 1 wrong order
    } else if (n1.value == null && n2.value != null) {
      // convert n2 value to list
      Node n2ToListNode = new Node(n2);
      n2ToListNode.value = n2.value;
      n2.value = null;
    } else if (n1.value != null && n2.value == null) {
      // convert n1 value to list
      Node n1ToListNode = new Node(n1);
      n1ToListNode.value = (int)n1.value;
      n1.value = null;
    } else {
      ; // both values already lists
    }

    // both values are now lists; compare item by item
    int length1 = n1.children.size();
    int length2 = n2.children.size();
    int lengthMin = Math.min(length1, length2);
    for (int i = 0; i < lengthMin; i++) {
      int listResult = compareNodes(n1.children.get(i), n2.children.get(i));
      if (listResult != 0) return listResult;
    }
    return Integer.signum(length1 - length2); // -1 right order, 1 wrong order
  }

  private static class Node implements Comparable<Node> {
    private Integer value;
    private List<Node> children;
    private Node parent;

    public Node(Node parent) {
      this.value = null;
      this.children = new ArrayList<Node>();
      this.parent = parent;
      this.parent.children.add(this);
    }

    public Node() {
      this.value = null;
      this.children = new ArrayList<Node>();
    }

    @Override
    public int compareTo(Node other) {
      return compareNodes(this, other);
    }

    public String toString() {
      if (this.value != null) {
        return String.valueOf(this.value);
      } else {
        String result = "[";
        boolean firstChild = true;
        for (Node child : children) {
          if (!firstChild) result += ",";
          result += child.toString();
          firstChild = false;
        }
        result += "]";
        return result;
      }
    }
  }
}