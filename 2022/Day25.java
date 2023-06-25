import java.lang.Math;
import java.util.HashMap;
import java.util.Map;

public class Day25 {
  static String INPUT_FILE = "2022day25input.txt";
  static String TEST_INPUT_FILE = "2022day25testinput.txt";

  static long BASE = 5L;

  static Map<Character, Long> charValues = new HashMap<Character, Long>();
  static {
    charValues.put('2',  2L);
    charValues.put('1',  1L);
    charValues.put('0',  0L);
    charValues.put('-', -1L);
    charValues.put('=', -2L);
  }

  static Map<Long, Character> valueChars = new HashMap<Long, Character>();
  static {
    valueChars.put( 2L, '2');
    valueChars.put( 1L, '1');
    valueChars.put( 0L, '0');
    valueChars.put(-1L, '-');
    valueChars.put(-2L, '=');
  }

  public static void main(String[] args) throws Exception {
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    assert sumSnafu(testRows).equals("2=-1=0");

    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    System.out.println("Day 25 part 1: " + sumSnafu(realRows));
  }

  private static String sumSnafu(String[] rows) {
    long total = 0L;
    for (String snafu : rows) {
      total += snafuToDecimal(snafu);
    }
    return decimalToSnafu(total);
  }

  private static long snafuToDecimal(String snafu) {
    long result = 0L;
    for (int i = 0; i < snafu.length(); i++) {
      int exponent = snafu.length() - 1 - i;
      long digitValue = charValues.get(snafu.charAt(i));
      result += (digitValue * (long)Math.pow(BASE, exponent));
    }
    return result;
  }

  private static String decimalToSnafu(long decimal) {
    StringBuilder result = new StringBuilder();
    long remainder = decimal;
    while (remainder > 0) {
      long digit = Math.floorMod(remainder + 2L, BASE) - 2L;
      result.append(valueChars.get(digit));
      remainder -= digit;
      remainder /= BASE;
    }
    return result.reverse().toString();
  }
}