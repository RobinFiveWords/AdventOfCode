import java.util.Arrays;

class Day08 {
  static String TEST_INPUT_FILE = "2022day08testinput.txt";
  static String INPUT_FILE = "2022day08input.txt";

  public static void main(String[] args) throws Exception {
    String[] testData = aocUtils.bufferLinesFromFile("2022day08testinput.txt");
    int[][] testArray = createArray(testData);
    assert countVisible(testArray) == 21;
    assert maxScenicScore(testArray) == 8;

    String[] realData = aocUtils.bufferLinesFromFile("2022day08input.txt");
    int[][] realArray = createArray(realData);

    int part1 = countVisible(realArray);
    System.out.println("Day 8 part 1: " + part1);

    int part2 = maxScenicScore(realArray);
    System.out.println("Day 8 part 2: " + part2);
  }

  private static int[][] createArray(String[] data) {
      int nrows = data.length;
      int ncols = data[0].length();
      int[][] result = new int[nrows][ncols];
      for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++) {
          result[i][j] = Character.getNumericValue(data[i].charAt(j));
        }
      }
      return result;
  }

  private static int countVisible(int[][] array) {
    int result = 0;
    int nrows = array.length;
    int ncols = array[0].length;
    for (int i = 0; i < nrows; i++) {
      for (int j = 0; j < ncols; j++) {
        if (isVisible(array, i, j)) result++;
      }
    }
    return result;
  }

  private static boolean isVisible(int[][] array, int i, int j) {
    int value = array[i][j];
    int nrows = array.length;
    int ncols = array[0].length;
    int visibleDirections = 4;

    // up
    for (int y = 0; y < i; y++) {
      if (value <= array[y][j]) {
        visibleDirections--;
        break;
      }
    }
    // down
    for (int y = i + 1; y < nrows; y++) {
      if (value <= array[y][j]) {
        visibleDirections--;
        break;
      }
    }
    // left
    for (int x = 0; x < j; x++) {
      if (value <= array[i][x]) {
        visibleDirections--;
        break;
      }
    }
    // right
    for (int x = j + 1; x < ncols; x++) {
      if (value <= array[i][x]) {
        visibleDirections--;
        break;
      }
    }

    return visibleDirections > 0;
  }

  private static int maxScenicScore(int[][] array) {
      int result = 0;
      int nrows = array.length;
      int ncols = array[0].length;
      for (int i = 1; i < nrows - 1; i++) {
        for (int j = 1; j < ncols - 1; j++) {
          int score = scenicScore(array, i, j);
          if (score > result) result = score;
        }
      }
      return result;
  }

  private static int scenicScore(int[][] array, int i, int j) {
    int value = array[i][j];
    int nrows = array.length;
    int ncols = array[0].length;

    int result = 1;
    int viewingDistance = 0;

    // up
    for (int y = i - 1; y >= 0; y--) {
      viewingDistance++;
      if (value <= array[y][j]) break;
    }
    result *= viewingDistance;
    viewingDistance = 0;
    // down
    for (int y = i + 1; y < nrows; y++) {
      viewingDistance++;
      if (value <= array[y][j]) break;
    }
    result *= viewingDistance;
    viewingDistance = 0;
    // left
    for (int x = j - 1; x >= 0; x--) {
      viewingDistance++;
      if (value <= array[i][x]) break;
    }
    result *= viewingDistance;
    viewingDistance = 0;
    // right
    for (int x = j + 1; x < ncols; x++) {
      viewingDistance++;
      if (value <= array[i][x]) break;
    }
    result *= viewingDistance;

    return result;
  }
}