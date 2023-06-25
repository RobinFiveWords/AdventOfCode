import java.util.HashMap;

public class Day02 {

    public static void main(String[] args) throws Exception {
        String[] data = aocUtils.readLinesFromFileIntoArray("2022day02input.txt");
        int part1 = do_part1(data);
        System.out.println("Day 2 part 1: " + part1);
        int part2 = do_part2(data);
        System.out.println("Day 2 part 2: " + part2);
    }

    private static int do_part1(String[] data) {
        HashMap<String, Integer> scores = new HashMap<String, Integer>();
        scores.put("A X", 1 + 3);
        scores.put("A Y", 2 + 6);
        scores.put("A Z", 3 + 0);
        scores.put("B X", 1 + 0);
        scores.put("B Y", 2 + 3);
        scores.put("B Z", 3 + 6);
        scores.put("C X", 1 + 6);
        scores.put("C Y", 2 + 0);
        scores.put("C Z", 3 + 3);

        int result = 0;
        for (int i = 0; i < data.length; i++) {
            result += scores.get(data[i]);
        }
        return result;
    }

    private static int do_part2(String[] data) {
        HashMap<String, Integer> scores = new HashMap<String, Integer>();
        scores.put("A X", 3 + 0);
        scores.put("A Y", 1 + 3);
        scores.put("A Z", 2 + 6);
        scores.put("B X", 1 + 0);
        scores.put("B Y", 2 + 3);
        scores.put("B Z", 3 + 6);
        scores.put("C X", 2 + 0);
        scores.put("C Y", 3 + 3);
        scores.put("C Z", 1 + 6);

        int result = 0;
        for (int i = 0; i < data.length; i++) {
            result += scores.get(data[i]);
        }
        return result;
    }
}