import java.lang.Math;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Day20 {
  static String INPUT_FILE = "2022day20input.txt";
  static String TEST_INPUT_FILE = "2022day20testinput.txt";

  static long DECRYPTION_KEY = 811589153L;

  public static void main(String[] args) throws Exception {
    String[] testRows = aocUtils.bufferLinesFromFile(TEST_INPUT_FILE);
    List<Long> testNums1 = parseRows(testRows);
    List<Integer> testIdxs1 = createIndices(testNums1);
    run(testNums1, testIdxs1);
    assert groveCoordinates(testNums1) == 3;

    List<Long> testNums2 = parseRows(testRows);
    scale(testNums2, DECRYPTION_KEY);
    List<Integer> testIdxs2 = createIndices(testNums2);
    for (int round = 0; round < 10; round++) {
      run(testNums2, testIdxs2);
    }
    assert groveCoordinates(testNums2) == 1623178306L;

    String[] realRows = aocUtils.bufferLinesFromFile(INPUT_FILE);
    List<Long> realNums1 = parseRows(realRows);
    List<Integer> realIdxs1 = createIndices(realNums1);
    run(realNums1, realIdxs1);
    System.out.println("Day 20 part 1: " + groveCoordinates(realNums1));

    List<Long> realNums2 = parseRows(realRows);
    scale(realNums2, DECRYPTION_KEY);
    List<Integer> realIdxs2 = createIndices(realNums2);
    for (int round = 0; round < 10; round++) {
      run(realNums2, realIdxs2);
    }
    System.out.println("Day 20 part 2: " + groveCoordinates(realNums2));
  }

  private static void run(List<Long> nums, List<Integer> idxs) {
    for (int mix = 0; mix < nums.size(); mix++) {
      move(mix, nums, idxs);
    }
  }

  private static void scale(List<Long> nums, long factor) {
    for (int index = 0; index < nums.size(); index++) {
      nums.set(index, nums.get(index) * factor);
    }
  }

  private static void move(int mix, List<Long> nums, List<Integer> idxs) {
    int index = idxs.indexOf(mix);
    Long num = nums.get(index);
    if (num == 0) return;
    int modulus = nums.size() - 1;
    int landsAt = (int)Math.floorMod(index + num, modulus);
    if (landsAt == index) return;
    if (landsAt == 0) landsAt = modulus;
    if (landsAt == index) return;

    if (landsAt > index) {
      Collections.rotate(nums.subList(index, landsAt + 1), -1);
      Collections.rotate(idxs.subList(index, landsAt + 1), -1);
    } else {
      Collections.rotate(nums.subList(landsAt, index + 1), 1);
      Collections.rotate(idxs.subList(landsAt, index + 1), 1);
    }
  }

  private static long groveCoordinates(List<Long> nums) {
    int startIdx = nums.indexOf(0L);
    long result = 0L;
    int[] idxs = {1000, 2000, 3000};
    for (int idx : idxs) {
      idx += startIdx;
      idx %= nums.size();
      result += nums.get(idx);
    }
    return result;
  }

  private static List<Long> parseRows(String[] rows) {
    List<Long> results = new ArrayList<Long>();
    for (String row : rows) {
      results.add(Long.parseLong(row));
    }
    return results;
  }

  private static List<Integer> createIndices(List<Long> nums) {
    List<Integer> results = new ArrayList<Integer>();
    for (int i = 0; i < nums.size(); i++) {
      results.add(i);
    }
    return results;
  }
}